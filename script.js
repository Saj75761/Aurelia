const API_URL = 'http://localhost:8000';

// ─── STATE MANAGEMENT ───
let cart = JSON.parse(localStorage.getItem('aurelia_cart')) || [];
let products = [];
let activeCategory = 'all';

// ─── INITIALIZATION ───
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
    setupIntersectionObserver();
    updateCartUI();
});

async function initApp() {
    await fetchProducts();
    if (document.getElementById('product-grid')) {
        renderProducts();
    }
}

// ─── FETCH DATA ───
async function fetchProducts() {
    try {
        const response = await fetch(`${API_URL}/products`);
        const data = await response.json();
        products = data.products;
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// ─── UI RENDERING ───
function renderProducts() {
    const grid = document.getElementById('product-grid');
    if (!grid) return;

    const filteredProducts = activeCategory === 'all' 
        ? products 
        : products.filter(p => p.category === activeCategory);

    grid.innerHTML = filteredProducts.map(product => `
        <div class="product-card reveal">
            ${product.badge ? `<div class="product-badge">${product.badge}</div>` : ''}
            <div class="product-image">
                <img src="${product.image_url}" alt="${product.name}" loading="lazy">
                <div class="product-overlay">
                    <button class="btn btn-outline" onclick="addToCart(${product.id})">Select for Atelier</button>
                </div>
            </div>
            <div class="product-info">
                <p class="product-category">${product.category}</p>
                <div class="product-name">
                    <span>${product.name}</span>
                    <span class="product-price">$${product.price.toLocaleString()}</span>
                </div>
                <p style="font-size: 0.85rem; color: #888; margin-top: 10px;">${product.description}</p>
            </div>
        </div>
    `).join('');
    
    // Refresh animations for newly rendered elements
    setTimeout(setupIntersectionObserver, 100);
}

// ─── FILTER LOGIC ───
function filterCategory(category) {
    activeCategory = category;
    
    // Update button states
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        if (btn.innerText.toLowerCase() === category.toLowerCase() || (category === 'all' && btn.innerText.toLowerCase() === 'all')) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    renderProducts();
}

// ─── CART LOGIC ───
function addToCart(id) {
    const product = products.find(p => p.id === id);
    if (!product) return;

    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    saveCart();
    updateCartUI();
    
    // Smoothly show cart section (drawer)
    setTimeout(() => {
        toggleCart(true);
    }, 300);
    
    // Trigger animation on cart icon
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.style.transform = 'scale(1.2)';
        setTimeout(() => cartIcon.style.transform = 'scale(1)', 200);
    }
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    updateCartUI();
}

function saveCart() {
    localStorage.setItem('aurelia_cart', JSON.stringify(cart));
}

function updateCartUI() {
    const countElements = document.querySelectorAll('.cart-count');
    const itemsContainer = document.querySelector('.cart-items');
    const totalEl = document.querySelector('.cart-total-value');
    
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    countElements.forEach(el => {
        el.innerText = totalItems;
    });

    // Handle floating cart visibility
    const floatingCart = document.getElementById('floating-cart');
    if (floatingCart) {
        if (totalItems > 0) {
            floatingCart.classList.add('visible');
        } else {
            floatingCart.classList.remove('visible');
        }
    }
    
    if (itemsContainer) {
        if (cart.length === 0) {
            itemsContainer.innerHTML = `
                <div style="text-align:center; padding: 100px 0;">
                    <p style="color: var(--gold); font-family: 'Playfair Display', serif; font-size: 1.5rem; margin-bottom: 20px;">Your Atelier is Empty</p>
                    <p style="color: #666; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase;">Awaiting your curation</p>
                </div>
            `;
        } else {
            itemsContainer.innerHTML = cart.map(item => `
                <div class="cart-item">
                    <img src="${item.image_url}" class="cart-item-img">
                    <div class="cart-item-details">
                        <h4>${item.name}</h4>
                        <p class="cart-item-price">${item.quantity} × $${item.price.toLocaleString()}</p>
                        <span class="remove-btn" onclick="removeFromCart(${item.id})">Remove from collection</span>
                    </div>
                </div>
            `).join('');
        }
    }

    if (totalEl) {
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        totalEl.innerText = `$${total.toLocaleString()}`;
    }
}

function toggleCart(open) {
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('overlay');
    if (open) {
        drawer.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    } else {
        drawer.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// ─── AI CONCIERGE LOGIC ───
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        
        setTimeout(() => {
            appendMessage('ai', data.response);
        }, 600);
    } catch (error) {
        console.error('Chat error:', error);
        appendMessage('ai', "My apologies, the atelier connection is momentarily unavailable.");
    }
}

function appendMessage(sender, text) {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    const msgEl = document.createElement('div');
    msgEl.className = `message ${sender}`;
    msgEl.innerText = text;
    container.appendChild(msgEl);
    container.scrollTop = container.scrollHeight;
}

function toggleChat() {
    const win = document.getElementById('chat-window');
    if (win) win.classList.toggle('active');
}

// ─── EVENT LISTENERS ───
function setupEventListeners() {
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        if (header) {
            if (window.scrollY > 80) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
    });

    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData.entries());
            
            const submitBtn = contactForm.querySelector('button');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = "Transmitting...";
            submitBtn.disabled = true;

            try {
                const response = await fetch(`${API_URL}/contact-submit`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                alert(result.message);
                contactForm.reset();
            } catch (error) {
                alert("The concierge is currently unavailable.");
            } finally {
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}

// ─── INTERSECTION OBSERVER ───
function setupIntersectionObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}
