from typing import Type

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class SuperUserMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users_list.html', context)

class UsersListView(SuperUserMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     return ShopUser.objects.filter(is_superuser=False)


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#     context = {
#         'form': user_form
#     }
#     return render(request, 'adminapp/user_form.html', context)

class UserCreateView(SuperUserMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         user_form = ShopUserAdminEditForm(instance=current_user)
#     context = {
#         'form': user_form
#     }
#     return render(request, 'adminapp/user_form.html', context)

class UserUpdateView(SuperUserMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserEditForm
    success_url = reverse_lazy('adminapp:users')


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         current_user.is_active = False
#         current_user.save()
#         return HttpResponseRedirect(reverse('adminapp:users'))
#
#     context = {
#         'object': current_user
#     }
#     return render(request, 'adminapp/user_delete.html', context)

class UserDeleteView(SuperUserMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     context = {
#         'object_list': ProductCategory.objects.all()
#     }
#
#     return render(request, 'adminapp/categories_list.html', context)

class ProductCategoriesListView(SuperUserMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'

# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'adminapp/category_form.html', context)


class ProductCategoryCreateView(SuperUserMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST, instance=category_item)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm(instance=category_item)
#     context = {
#         'form': form
#     }
#     return render(request, 'adminapp/category_form.html', context)

class ProductCategoryUpdateView(SuperUserMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     current_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         current_category.is_active = False
#         current_category.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#
#     context = {
#         'object': current_category
#     }
#     return render(request, 'adminapp/category_delete.html', context)

class ProductCategoryDeleteView(SuperUserMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     context = {
#         'category': category,
#         'object_list': Product.objects.filter(category__pk=pk)
#     }
#
#     return render(request, 'adminapp/products_list.html', context)

class ProductsListView(SuperUserMixin, ListView):
    model = Product
    template_name = 'adminapp/products_list.html'

    def get_category(self):
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context_data['category'] = self.get_category()
            context_data['object_list'] = Product.objects.filter(category__pk=self.get_category().pk)
        return context_data
# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', kwargs={'pk': category.pk}))
#     else:
#         product_form = ProductForm(
#             initial={
#                 'category': category
#             }
#         )
#     context = {
#         'product_form': product_form,
#         'category': category
#     }
#     return render(request, 'adminapp/product_form.html', context)


class ProductCreateView(SuperUserMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm
    # success_url = reverse_lazy('adminnapp:categories')

    def get_category(self):
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context_data['category'] = self.get_category()
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES, instance=product)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', kwargs={'pk': product.category.pk}))
#     else:
#         product_form = ProductForm(instance=product)
#     context = {
#         'product_form': product_form,
#         'category': product.category
#     }
#     return render(request, 'adminapp/product_form.html', context)

class ProductUpdateView(SuperUserMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm
    # success_url = reverse_lazy('adminnapp:categories')

    def get_category(self):
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context_data['category'] = self.get_category()
        return context_data

# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('adminapp:products', kwargs={'pk': product.category.pk}))
#
#     context = {
#         'product': product
#     }
#     return render(request, 'adminapp/product_delete.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'object': product
#     }
#     return render(request, 'adminapp/product_read.html', context)
class ProductDeleteView(SuperUserMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    # success_url = reverse_lazy('adminapp:categories')

    def get_category(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        category_item = product.category
        return category_item

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context_data['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return context_data


class ProductDetailView(SuperUserMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
