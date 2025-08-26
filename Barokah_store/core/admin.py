# core/admin.py
from django.contrib import admin
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Avg


## Tampilan Admin untuk Produk
# -------------------------------------------------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'image_tag', 'average_rating')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')
    list_per_page = 20

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = 'Image'
    
    def average_rating(self, obj):
        # Menghitung rata-rata rating dari semua ulasan produk
        avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return f'{avg_rating:.2f} / 5'
        return 'N/A'
    average_rating.short_description = 'Rating'

## Tampilan Admin untuk Order Item (Inline)
# -------------------------------------------------------------------------------------------------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    readonly_fields = ('price',)
    extra = 0


## Tampilan Admin untuk Order (Verifikasi & Status)
# -------------------------------------------------------------------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Menyisipkan detail order di halaman yang sama
    inlines = [OrderItemInline]
    
    # Menambahkan tombol aksi untuk verifikasi pembayaran
    actions = ['mark_as_paid']

    # Kolom di halaman daftar pesanan
    list_display = ('id', 'customer', 'date_ordered', 'total_price', 'payment_status', 'payment_proof_tag')
    list_filter = ('payment_status', 'date_ordered')
    search_fields = ('customer__username', 'customer__email')
    list_per_page = 20
    
    # Kolom yang hanya bisa dibaca
    readonly_fields = ('date_ordered', 'payment_proof_tag', 'customer', 'total_price')

    # Fungsi untuk menampilkan preview bukti pembayaran
    def payment_proof_tag(self, obj):
        if obj.payment_proof_image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />'.format(obj.payment_proof_image.url))
        return "No Proof"
    payment_proof_tag.short_description = 'Payment Proof'
    
    # Aksi kustom untuk mengubah status pembayaran menjadi 'Paid'
    def mark_as_paid(self, request, queryset):
        queryset.update(payment_status='Paid')
    mark_as_paid.short_description = "Tandai sebagai sudah dibayar"


## Tampilan Admin untuk User
# -------------------------------------------------------------------------------------------------------------------
# Hapus pendaftaran User bawaan dari Django Admin
admin.site.unregister(User)

# Mendaftarkan kembali model User dengan penyesuaian
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    
    



   