# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import ProcessFormView, UpdateView, DeleteView

from .forms import GoodFormCustomFields, GoodFormMetaEditing
from .models import Category, Good


# class GoodListView(TemplateView):
# 	template_name = "index.html"
#
# 	def get_context_data(self, **kwargs):
# 		context = super(GoodListView, self).get_context_data(**kwargs)
# 		try:
# 			page_num = self.request.GET["page"]
# 		except KeyError:
# 			page_num = 1
#
# 		context["cats"] = Category.objects.all()
# 		context["category"] = (Category.objects.first() if kwargs["cat_id"] is None
# 		                       else Category.objects.get(pk=kwargs.get("cat_id")))
# 		pgtor = Paginator(Good.objects.filter(category=context["category"]).order_by("name"), 1)
# 		try:
# 			context["goods"] = pgtor.page(page_num)
# 		except InvalidPage:
# 			context["goods"] = pgtor.page(1)
# 		return context


# class GoodDetailView(TemplateView):
# 	template_name = "good.html"
#
# 	def get_context_data(self, **kwargs):
# 		context = super(GoodDetailView, self).get_context_data(**kwargs)
# 		try:
# 			context["pn"] = self.request.GET["page"]
# 		except KeyError:
# 			context["pn"] = 1
#
# 		context["cats"] = Category.objects.all()
# 		try:
# 			context["good"] = Good.objects.get(pk=kwargs.get("good_id"))
# 		except Good.DoesNotExist:
# 			raise Http404
# 		return context

class CategoryContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CategoryContextMixin, self).get_context_data(**kwargs)
        context["cats"] = Category.objects.all()
        return context


class GoodListView(ListView, CategoryContextMixin):
    template_name = "index.html"
    paginate_by = 5
    cat = None

    def get(self, request, *args, **kwargs):
        self.cat = Category.objects.first() if (self.kwargs["cat_id"] is None)\
            else Category.objects.get(pk=self.kwargs["cat_id"])
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context["category"] = self.cat
        return context

    def get_queryset(self):
        return Good.objects.filter(category=self.cat).order_by("name")


class GoodDetailView(DetailView, CategoryContextMixin):
    template_name = "good.html"
    model = Good
    pk_url_kwarg = "good_id"

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        context["pn"] = self.request.GET.get("page", 1)
        return context


# ----------------------------------------------------------------------------------------------------------------------

class GoodEditMixin(CategoryContextMixin):
    def get_context_data(self, **kwargs):
        context = super(GoodEditMixin, self).get_context_data(**kwargs)
        context["pn"] = self.request.GET.get("page", 1)
        return context


class GoodEditView(ProcessFormView):
    def post(self, request, *args, **kwargs):
        pn = request.GET.get("page", 1)
        self.success_url = "{}?page={}".format(self.success_url, pn)
        return super(GoodEditView, self).post(request, *args, **kwargs)


# class GoodCreate(CreateView, GoodEditMixin):
# 	model = Good
# 	template_name = "good_add.html"
# 	form_class = GoodFormCustomFields  # custom form using in CreateView
#
# 	def get(self, request, *args, **kwargs):
# 		if self.kwargs["cat_id"] is not None:
# 			self.initial["category"] = Category.objects.get(pk=self.kwargs["cat_id"])
# 		return super(GoodCreate, self).get(request, *args, **kwargs)
#
# 	def post(self, request, *args, **kwargs):
# 		self.success_url = reverse("index", kwargs={
# 			"cat_id": Category.objects.get(pk=self.kwargs["cat_id"]).id})
# 		return super(GoodCreate, self).post(request, *args, **kwargs)
#
# 	def get_context_data(self, **kwargs):
# 		context = super(GoodCreate, self).get_context_data(**kwargs)
# 		context["category"] = Category.objects.get(pk=self.kwargs["cat_id"])
# 		return context


class GoodCreate(TemplateView):
    """This is example of using simple template with custom form.
    Just add form object to context and process form in post method
    """

    form = None
    template_name = "good_add.html"
    cat = None

    def get(self, request, *args, **kwargs):
        self.cat = Category.objects.first() if (self.kwargs["cat_id"] is None)\
            else Category.objects.get(pk=self.kwargs["cat_id"])
        self.form = GoodFormCustomFields(initial={"category": self.cat})
        return super(GoodCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCreate, self).get_context_data(**kwargs)
        context["form"] = self.form
        context["category"] = self.cat
        return context

    def post(self, request, *args, **kwargs):
        cat = Category.objects.first() if (self.kwargs["cat_id"] is None)\
            else Category.objects.get(pk=self.kwargs["cat_id"])
        self.form = GoodFormCustomFields(request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.add_message(request, messages.SUCCESS, "Товар успешно добавлен")
            return redirect("index", cat_id=cat.id)
        else:
            return super(GoodCreate, self).get(request, *args, **kwargs)


class GoodUpdate(UpdateView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = "good_edit.html"
    pk_url_kwarg = "good_id"
    # fields = "__all__"
    form_class = GoodFormMetaEditing

    def post(self, request, *args, **kwargs):
        self.success_url = reverse("index", kwargs={
            "cat_id": Good.objects.get(pk=kwargs["good_id"]).category.id,
        })
        return super(GoodUpdate, self).post(request, *args, **kwargs)


class GoodDelete(DeleteView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = "good_delete.html"
    pk_url_kwarg = "good_id"

    def post(self, request, *args, **kwargs):
        self.success_url = reverse("index", kwargs={
            "cat_id": Good.objects.get(pk=kwargs["good_id"]).category.id,
        })
        return super(GoodDelete, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodDelete, self).get_context_data(**kwargs)
        context["good"] = Good.objects.get(pk=kwargs.get("good_id", 1))
        return context
