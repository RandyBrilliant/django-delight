from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Ingredient, Purchase, MenuItem, RecipeRequirement
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import IngredientForm, MenuForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models import Sum

# Create your views here.
@login_required
def home(request):
    ingredients = Ingredient.objects.all()[:5]
    purchases = Purchase.objects.all().order_by('-timestamp')[:5]
    menus = MenuItem.objects.all()[:5]
    context = {
        'ingredients': ingredients,
        'purchases': purchases,
        'menus': menus,
    }
    return render(request, "inventory/home.html", context)


class ListIngredient(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"
    context_object_name = "ingredients"


class CreateIngredient(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/ingredient_add.html"
    success_url = reverse_lazy('ingredient')


class UpdateIngredient(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/ingredient_add.html"
    success_url = reverse_lazy('ingredient')


class DeleteIngredient(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete.html"
    success_url = reverse_lazy('ingredient')


class ListMenu(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu_item.html"
    context_object_name = "menus"


# class CreateMenu(LoginRequiredMixin, CreateView):
#     model = MenuItem
#     form_class = MenuForm
#     template_name = "inventory/menu_item_add.html"


class CreateMenu(LoginRequiredMixin, TemplateView):
    template_name = "inventory/menu_item_add.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['ingredients'] = Ingredient.objects.all()
        return context
    
    def post(self, request):
        name = request.POST['menu_name']
        price = request.POST['menu_price']
        image = request.FILES['menu_image']
        menu_item = MenuItem(name=name, price=price, image=image)
        menu_item.save()

        ingredients_list = enumerate(request.POST.getlist('ingredient[]'), start=0)
        ingredients_qty = request.POST.getlist('ingredient_qty[]')

        menu = MenuItem.objects.get(name=name)

        for i, ingredient_name in ingredients_list:
            RecipeRequirement.objects.create(menu_item=menu, ingredient_id=ingredient_name, qty=ingredients_qty[i])

        return redirect("menu-item")
        


class UpdateMenu(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "inventory/menu_item_update.html"
    form_class = MenuForm
    success_url = reverse_lazy('menu-item')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['ingredients'] = Ingredient.objects.all()
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()

        ingredients_list = enumerate(request.POST.getlist('ingredient[]'), start=0)
        ingredients_qty = request.POST.getlist('ingredient_qty[]')

        menu = MenuItem.objects.get(name=self.object.name)

        menu.reciperequirement_set.all().delete()

        for i, ingredient_name in ingredients_list:
            RecipeRequirement.objects.create(menu_item=menu, ingredient_id=ingredient_name, qty=ingredients_qty[i])
        
        return super(UpdateMenu, self).post(request, **kwargs)


class DeleteMenu(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/menu_item_delete.html"
    success_url = reverse_lazy('menu-item')


class ListPurchase(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase.html"
    context_object_name = "purchases"
    ordering = ['-timestamp']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.unit_price * \
                    recipe_requirement.qty
        
        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost

        return context


class CreatePurchase(LoginRequiredMixin, TemplateView):
    template_name = "inventory/purchase_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = [X for X in MenuItem.objects.all() if X.available()]
        return context
    
    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.qty -= requirement.qty
            required_ingredient.save()
        
        purchase.save()
        return redirect("/purchase")



def sign_out(request):
    logout(request)
    return redirect('/')
