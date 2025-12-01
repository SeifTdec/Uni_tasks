const store = {
    products: [
        { id: 1, title: 'Wireless Bluetooth Headphones', category: 'electronics', price: 79.99, rating: 4.5, description: 'High-quality wireless headphones with noise cancellation and 30-hour battery life.' },
        { id: 2, title: 'Premium Cotton T-Shirt', category: 'clothing', price: 24.99, rating: 4.3, description: 'Comfortable, breathable cotton t-shirt available in multiple colors.' },
        { id: 3, title: 'The Great Novel', category: 'books', price: 14.99, rating: 4.7, description: 'A captivating story that will keep you reading until the end.' },
        { id: 4, title: 'Stainless Steel Cookware Set', category: 'home', price: 129.99, rating: 4.6, description: 'Professional-grade 10-piece cookware set for all your cooking needs.' },
        { id: 5, title: 'Yoga Mat Premium', category: 'sports', price: 34.99, rating: 4.4, description: 'Non-slip, eco-friendly yoga mat with carrying strap.' },
        { id: 6, title: 'Smart Watch Pro', category: 'electronics', price: 299.99, rating: 4.8, description: 'Advanced fitness tracking, heart rate monitor, and smartphone notifications.' },
        { id: 7, title: 'Designer Jeans', category: 'clothing', price: 89.99, rating: 4.2, description: 'Stylish and comfortable denim jeans with a modern fit.' },
        { id: 8, title: 'Cookbook Collection', category: 'books', price: 29.99, rating: 4.5, description: 'Over 200 delicious recipes from around the world.' },
        { id: 9, title: 'Coffee Maker Deluxe', category: 'home', price: 79.99, rating: 4.7, description: 'Programmable coffee maker with thermal carafe and auto-brew.' },
        { id: 10, title: 'Running Shoes', category: 'sports', price: 119.99, rating: 4.6, description: 'Lightweight, cushioned running shoes for maximum comfort.' },
        { id: 11, title: '4K Webcam', category: 'electronics', price: 149.99, rating: 4.4, description: 'Ultra HD webcam with auto-focus and built-in microphone.' },
        { id: 12, title: 'Winter Jacket', category: 'clothing', price: 159.99, rating: 4.5, description: 'Warm, waterproof jacket perfect for cold weather.' },
        { id: 13, title: 'Mystery Thriller Book', category: 'books', price: 12.99, rating: 4.3, description: 'A gripping mystery that will keep you guessing.' },
        { id: 14, title: 'Blender Pro 3000', category: 'home', price: 99.99, rating: 4.8, description: 'Powerful blender for smoothies, soups, and more.' },
        { id: 15, title: 'Tennis Racket', category: 'sports', price: 89.99, rating: 4.5, description: 'Professional-grade tennis racket with graphite frame.' }
    ],
    cart: [],
    currentCategory: 'all',
    searchQuery: '',
    sortBy: 'featured'
};

const utils = {
    formatPrice(price) {
        return `$${price.toFixed(2)}`;
    },
    formatRating(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        let stars = '⭐'.repeat(fullStars);
        if (hasHalfStar) stars += '⭐';
        return `${stars} (${rating})`;
    },
    saveCart() {
        // work in porgress when backend is done
    }
};

const productManager = {
    filterProducts() {
        let filtered = store.products;
        if (store.currentCategory !== 'all') {
            filtered = filtered.filter(p => p.category === store.currentCategory);
        }
        if (store.searchQuery) {
            const query = store.searchQuery.toLowerCase();
            filtered = filtered.filter(p => 
                p.title.toLowerCase().includes(query) || 
                p.description.toLowerCase().includes(query)
            );
        }
        switch(store.sortBy) {
            case 'price-low':
                filtered.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                filtered.sort((a, b) => b.price - a.price);
                break;
            case 'rating':
                filtered.sort((a, b) => b.rating - a.rating);
                break;
        }
        return filtered;
    },
    
    renderProducts() {
        const grid = document.getElementById('productsGrid');
        const products = this.filterProducts();
        grid.innerHTML = products.map(product => `
            <div class="product-card" data-id="${product.id}">
                <div class="product-image">Place holder product</div>
                <div class="product-info">
                    <div class="product-category">${product.category}</div>
                    <div class="product-title">${product.title}</div>
                    <div class="product-rating">${utils.formatRating(product.rating)}</div>
                    <div class="product-price">${utils.formatPrice(product.price)}</div>
                    <button class="add-to-cart-btn" data-id="${product.id}">Add to Cart</button>
                </div>
            </div>
        `).join('');
        
        this.attachProductEventListeners();
    },
    
    attachProductEventListeners() {
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.classList.contains('add-to-cart-btn')) {
                    const id = parseInt(card.dataset.id);
                    this.showProductDetail(id);
                }
            });
        });
        
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = parseInt(btn.dataset.id);
                cartManager.addToCart(id);
            });
        });
    },
    
    showProductDetail(id) {
        const product = store.products.find(p => p.id === id);
        if (!product) return;
        
        const detailContainer = document.getElementById('productDetail');
        detailContainer.innerHTML = `
            <div class="product-detail-image">Place holder product</div>
            <div class="product-detail-info">
                <div class="product-detail-category">${product.category}</div>
                <h2>${product.title}</h2>
                <div class="product-detail-rating">${utils.formatRating(product.rating)}</div>
                <div class="product-detail-price">${utils.formatPrice(product.price)}</div>
                <div class="product-detail-description">${product.description}</div>
                <button class="add-to-cart-btn" data-id="${product.id}">Add to Cart</button>
            </div>
        `;
        detailContainer.querySelector('.add-to-cart-btn').addEventListener('click', () => {
            cartManager.addToCart(id);
        });
        modalManager.openModal('productModal');
    }
};


const cartManager = {
    addToCart(productId) {
        const product = store.products.find(p => p.id === productId);
        if (!product) return;
        
        const existingItem = store.cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity++;
        } else {
            store.cart.push({ ...product, quantity: 1 });
        }
        
        this.updateCartCount();
        utils.saveCart();
        this.showNotification('Added to cart!');
    },
    
    removeFromCart(productId) {
        store.cart = store.cart.filter(item => item.id !== productId);
        this.updateCartCount();
        this.renderCart();
        utils.saveCart();
    },
    
    updateQuantity(productId, change) {
        const item = store.cart.find(item => item.id === productId);
        if (!item) return;
        
        item.quantity += change;
        
        if (item.quantity <= 0) {
            this.removeFromCart(productId);
        } else {
            this.updateCartCount();
            this.renderCart();
            utils.saveCart();
        }
    },
    
    updateCartCount() {
        const count = store.cart.reduce((sum, item) => sum + item.quantity, 0);
        document.getElementById('cartCount').textContent = count;
    },
    
    renderCart() {
        const cartItemsContainer = document.getElementById('cartItems');
        const cartSummaryContainer = document.getElementById('cartSummary');
        
        if (store.cart.length === 0) {
            cartItemsContainer.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
            cartSummaryContainer.innerHTML = '';
            return;
        }
        
        cartItemsContainer.innerHTML = store.cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">Item I guess</div>
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-price">${utils.formatPrice(item.price)}</div>
                    <div class="cart-item-controls">
                        <button class="quantity-btn" data-id="${item.id}" data-action="decrease">-</button>
                        <span class="quantity-display">${item.quantity}</span>
                        <button class="quantity-btn" data-id="${item.id}" data-action="increase">+</button>
                        <button class="remove-btn" data-id="${item.id}">Remove</button>
                    </div>
                </div>
            </div>
        `).join('');
        
        const total = store.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        cartSummaryContainer.innerHTML = `
            <div class="cart-total">
                <span>Total:</span>
                <span>${utils.formatPrice(total)}</span>
            </div>
            <button class="checkout-btn" id="checkoutBtn">Proceed to Checkout</button>
        `;
        
        this.attachCartEventListeners();
    },
    
    attachCartEventListeners() {
        document.querySelectorAll('.quantity-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = parseInt(btn.dataset.id);
                const action = btn.dataset.action;
                const change = action === 'increase' ? 1 : -1;
                this.updateQuantity(id, change);
            });
        });
        
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = parseInt(btn.dataset.id);
                this.removeFromCart(id);
            });
        });
        const checkoutBtn = document.getElementById('checkoutBtn');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => {
                this.checkout();
            });
        }
    },
    
    checkout() {
        alert('work in porgress when backend is done');
        store.cart = [];
        this.updateCartCount();
        this.renderCart();
        utils.saveCart();
    },
    
    showNotification(message) {
        // Simple notification - could be enhanced with a proper notification system
        const existingNotif = document.querySelector('.notification');
        if (existingNotif) existingNotif.remove();
        
        const notif = document.createElement('div');
        notif.className = 'notification';
        notif.textContent = message;
        notif.style.cssText = 'position:fixed;top:80px;right:20px;background:#329d9c;color:white;padding:1rem 2rem;border-radius:4px;z-index:3000;box-shadow:0 4px 8px rgba(0,0,0,0.2);';
        document.body.appendChild(notif);
        
        setTimeout(() => notif.remove(), 2000);
    }
};

const modalManager = {
    openModal(modalId) {
        document.getElementById(modalId).classList.add('active');
        document.body.style.overflow = 'hidden';
    },
    
    closeModal(modalId) {
        document.getElementById(modalId).classList.remove('active');
        document.body.style.overflow = 'auto';
    },
    
    init() {
        document.getElementById('closeProductModal').addEventListener('click', () => {
            this.closeModal('productModal');
        });
        
        document.getElementById('closeCartModal').addEventListener('click', () => {
            this.closeModal('cartModal');
        });
        
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal.id);
                }
            });
        });
    }
};

function initEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    
    searchBtn.addEventListener('click', () => {
        store.searchQuery = searchInput.value;
        productManager.renderProducts();
    });
    
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            store.searchQuery = searchInput.value;
            productManager.renderProducts();
        }
    });
    
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            store.currentCategory = btn.dataset.category;
            productManager.renderProducts();
        });
    });
    
    document.getElementById('sortSelect').addEventListener('change', (e) => {
        store.sortBy = e.target.value;
        productManager.renderProducts();
    });
    
    document.getElementById('cartBtn').addEventListener('click', () => {
        cartManager.renderCart();
        modalManager.openModal('cartModal');
    });
}


function init() {
    productManager.renderProducts();
    cartManager.updateCartCount();
    modalManager.init();
    initEventListeners();
}


if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}