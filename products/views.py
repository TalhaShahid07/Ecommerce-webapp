from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.paginator import Paginator
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'page_obj'  # Use 'page_obj' for pagination

    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        products = Product.objects.all()

        if query:
            products = products.filter(title__icontains=query)
        if category:
            products = products.filter(category__name=category)
        if price_min:
            products = products.filter(price__gte=price_min)
        if price_max:
            products = products.filter(price__lte=price_max)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['page_obj'], 10)  # Show 10 products per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['title', 'description', 'price', 'category', 'image']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

    def test_func(self):
        return self.request.user.is_superuser

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'description', 'price', 'category', 'image']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

    def test_func(self):
        return self.request.user.is_superuser

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

    def test_func(self):
        return self.request.user.is_superuser
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm

def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product-detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'products/add_review.html', {'form': form, 'product': product})
