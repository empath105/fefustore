from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from .models import Category, Product, CartItem, Order, OrderItem 
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CartItemSerializer, 
    OrderSerializer,
    RegisterSerializer
)

class CategoryListCreateAPI(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Доступ запрещен. Требуются права администратора.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPI(APIView):
    def put(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Передаем partial=True, чтобы можно было изменять только имя
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({'success': True, 'detail': 'Категория удалена'}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)

class ProductListCreateAPI(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        queryset = Product.objects.filter(is_active=True)

        category_slug = request.query_params.get('category')
        search_query = request.query_params.get('search')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if search_query:
            queryset = queryset.filter(
                models.Q(name__icontains=search_query) | 
                models.Q(description__icontains=search_query)
            )

        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Доступ запрещен. Требуются права администратора.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPI(APIView):
    serializer_class = ProductSerializer

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'success': True, 'detail': 'Товар удален'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)


class CartAPI(APIView):
    serializer_class = CartItemSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт, чтобы посмотреть корзину.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        
        cart_total_price = sum(item.quantity * item.product.price for item in cart_items)
        
        return Response({
            'items': serializer.data,
            'cart_total_price': cart_total_price
        }, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт, чтобы добавлять товары.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data.get('quantity', 1)

            try:
                product = Product.objects.get(pk=product_id, is_active=True)
            except Product.DoesNotExist:
                return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
          
            return self.get(request)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetailAPI(APIView):
    serializer_class = CartItemSerializer

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Элемент корзины не найден'}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity is None or int(quantity) <= 0:
            return Response({'error': 'Количество должно быть больше 0'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = int(quantity)
        cart_item.save()

        cart_items = CartItem.objects.filter(user=request.user)
        cart_total_price = sum(item.quantity * item.product.price for item in cart_items)
        return Response({
            'items': CartItemSerializer(cart_items, many=True).data,
            'cart_total_price': cart_total_price
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Элемент корзины не найден'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        cart_items = CartItem.objects.filter(user=request.user)
        cart_total_price = sum(item.quantity * item.product.price for item in cart_items)
        return Response({
            'items': CartItemSerializer(cart_items, many=True).data,
            'cart_total_price': cart_total_price
        }, status=status.HTTP_200_OK)

class OrderListCreateAPI(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт, чтобы просмотреть заказы.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
            
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт, чтобы оформить заказ.'}, status=status.HTTP_401_UNAUTHORIZED)

        cart_items = CartItem.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return Response({'error': 'Ваша корзина пуста. Нечего оформлять.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.quantity * item.product.price for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPI(APIView):
    serializer_class = OrderSerializer

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'detail': 'Войдите в аккаунт.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            if request.user.is_staff:
                order = Order.objects.get(pk=pk)
            else:
                order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Доступ запрещен. Требуются права администратора.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
    
        available_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in available_statuses:
            return Response(
                {'error': f'Недопустимый статус. Выберите из: {available_statuses}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Пользователь успешно зарегистрирован. Теперь вы можете войти."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)