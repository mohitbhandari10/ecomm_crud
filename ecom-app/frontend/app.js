const API_BASE = 'http://localhost:8000';

// Auth functions
let currentUser = JSON.parse(localStorage.getItem('currentUser'));

function updateAuthUI() {
    const authLinks = document.getElementById('auth-links');
    const userLinks = document.getElementById('user-links');
    const userEmail = document.getElementById('user-email');
    const addProductBtn = document.getElementById('addProductBtn');

    if (currentUser) {
        if (authLinks) authLinks.style.display = 'none';
        if (userLinks) userLinks.style.display = 'inline';
        if (userEmail) userEmail.textContent = currentUser.email;
        if (addProductBtn && currentUser.is_admin) {
            addProductBtn.style.display = 'block';
        }
    } else {
        if (authLinks) authLinks.style.display = 'inline';
        if (userLinks) userLinks.style.display = 'none';
        if (addProductBtn) addProductBtn.style.display = 'none';
    }
}

async function register(e) {
    if (e) e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        showMessage('Passwords do not match', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Registration successful! Please login.', 'success');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showMessage(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    }
}

async function login(e) {
    if (e) e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = {
                email: email,
                token: data.access_token,
                is_admin: data.is_admin
            };
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            showMessage('Login successful!', 'success');
            setTimeout(() => {
                window.location.href = 'products.html';
            }, 1000);
        } else {
            showMessage(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    }
}

function logout() {
    localStorage.removeItem('currentUser');
    currentUser = null;
    window.location.href = 'index.html';
}

// Product functions
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        const products = await response.json();

        const productsList = document.getElementById('productsList');
        productsList.innerHTML = '';

        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';
            productCard.innerHTML = `
                <h3>${product.name}</h3>
                <p>${product.description}</p>
                <div class="price">$${product.price}</div>
                <div class="stock">Stock: ${product.stock}</div>
                ${currentUser && currentUser.is_admin ? `
                    <div class="product-actions">
                        <button class="btn btn-primary" onclick="editProduct(${product.id})">Edit</button>
                        <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Delete</button>
                    </div>
                ` : ''}
            `;
            productsList.appendChild(productCard);
        });
    } catch (error) {
        showMessage('Error loading products: ' + error.message, 'error');
    }
}

function showProductForm() {
    document.getElementById('adminPanel').style.display = 'block';
    document.getElementById('productId').value = '';
    document.getElementById('productForm').reset();
}

function cancelEdit() {
    document.getElementById('adminPanel').style.display = 'none';
    document.getElementById('productId').value = '';
    document.getElementById('productForm').reset();
}

async function saveProduct(e) {
    e.preventDefault();

    if (!currentUser || !currentUser.is_admin) {
        showMessage('You need to be an admin to perform this action', 'error');
        return;
    }

    const productId = document.getElementById('productId').value;
    const productData = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        price: parseFloat(document.getElementById('price').value),
        stock: parseInt(document.getElementById('stock').value)
    };

    try {
        const url = productId ? `${API_BASE}/products/${productId}` : `${API_BASE}/products`;
        const method = productId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentUser.token}`
            },
            body: JSON.stringify(productData)
        });

        if (response.ok) {
            showMessage(`Product ${productId ? 'updated' : 'created'} successfully!`, 'success');
            cancelEdit();
            loadProducts();
        } else {
            const data = await response.json();
            showMessage(data.detail || 'Operation failed', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    }
}

async function editProduct(productId) {
    try {
        const response = await fetch(`${API_BASE}/products`);
        const products = await response.json();
        const product = products.find(p => p.id === productId);

        if (product) {
            document.getElementById('adminPanel').style.display = 'block';
            document.getElementById('productId').value = product.id;
            document.getElementById('name').value = product.name;
            document.getElementById('description').value = product.description;
            document.getElementById('price').value = product.price;
            document.getElementById('stock').value = product.stock;
        }
    } catch (error) {
        showMessage('Error loading product: ' + error.message, 'error');
    }
}

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/products/${productId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${currentUser.token}`
            }
        });

        if (response.ok) {
            showMessage('Product deleted successfully!', 'success');
            loadProducts();
        } else {
            const data = await response.json();
            showMessage(data.detail || 'Delete failed', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    }
}

// Utility functions
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    updateAuthUI();

    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', register);
    }

    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', login);
    }

    // Product form
    const productForm = document.getElementById('productForm');
    if (productForm) {
        productForm.addEventListener('submit', saveProduct);
    }

    // Add product button
    const addProductBtn = document.getElementById('addProductBtn');
    if (addProductBtn) {
        addProductBtn.addEventListener('click', showProductForm);
    }

    // Load products on products page
    if (window.location.pathname.includes('products.html')) {
        loadProducts();
    }
});