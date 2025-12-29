// /**
//  * Shop Boxes Page Logic
//  * Handles mock data, filtering, sorting, and rendering.
//  */

// document.addEventListener('DOMContentLoaded', () => {

//     // --- Mock Data ---
//     const boxes = [
//         {
//             id: 1,
//             name: "Premium Magnetic Gift Box",
//             type: "Standard Box",
//             occasion: "Corporate",
//             material: "Cardboard",
//             sizes: ["Small", "Medium", "Large"],
//             prices: { "Small": 1200, "Medium": 1800, "Large": 2500 },
//             image: "https://placehold.co/400x400/212529/fff?text=Magnetic+Box",
//             inStock: true,
//             stockCount: 50,
//             rating: 4.8,
//             reviews: 124,
//             isNew: true,
//             description: "Luxurious rigid box with magnetic closure. Perfect for corporate gifting."
//         },
//         {
//             id: 2,
//             name: "Handwoven Wicker Basket",
//             type: "Basket",
//             occasion: "Festival",
//             material: "Wicker/Rattan",
//             sizes: ["Medium", "Large", "Extra Large"],
//             prices: { "Medium": 2500, "Large": 3500, "Extra Large": 4500 },
//             image: "https://placehold.co/400x400/8d6e63/fff?text=Wicker+Basket",
//             inStock: true,
//             stockCount: 15,
//             rating: 4.9,
//             reviews: 85,
//             isNew: false,
//             description: "Traditional handwoven wicker basket. Ideal for festive hampers."
//         },
//         {
//             id: 3,
//             name: "Rustic Wooden Crate",
//             type: "Wooden Crate",
//             occasion: "Birthday",
//             material: "Wood",
//             sizes: ["Small", "Medium"],
//             prices: { "Small": 1500, "Medium": 2200 },
//             image: "https://placehold.co/400x400/deb887/fff?text=Wooden+Crate",
//             inStock: true,
//             stockCount: 8, // Low stock
//             rating: 4.7,
//             reviews: 42,
//             isNew: false,
//             description: "Sturdy wooden crate with a rustic finish. Great for organic products."
//         },
//         {
//             id: 4,
//             name: "Heart Shaped Tin",
//             type: "Heart-shaped Box",
//             occasion: "Anniversary",
//             material: "Metal/Tin",
//             sizes: ["Small"],
//             prices: { "Small": 800 },
//             image: "https://placehold.co/400x400/dc3545/fff?text=Heart+Tin",
//             inStock: true,
//             stockCount: 25,
//             rating: 4.5,
//             reviews: 30,
//             isNew: false,
//             description: "Romantic heart-shaped tin container. Perfect for chocolates and small gifts."
//         },
//         {
//             id: 5,
//             name: "Elegant Cylinder Box",
//             type: "Cylinder Box",
//             occasion: "Wedding",
//             material: "Cardboard",
//             sizes: ["Medium", "Large"],
//             prices: { "Medium": 1600, "Large": 2100 },
//             image: "https://placehold.co/400x400/f8f9fa/333?text=Cylinder+Box",
//             inStock: false,
//             stockCount: 0,
//             rating: 4.6,
//             reviews: 18,
//             isNew: true,
//             description: "Modern cylindrical box with gold accents. Adds a touch of elegance."
//         },
//         {
//             id: 6,
//             name: "Festive Tin Trunk",
//             type: "Tin Container",
//             occasion: "Festival",
//             material: "Metal/Tin",
//             sizes: ["Medium", "Large"],
//             prices: { "Medium": 1800, "Large": 2400 },
//             image: "https://placehold.co/400x400/ffc107/fff?text=Tin+Trunk",
//             inStock: true,
//             stockCount: 12,
//             rating: 4.4,
//             reviews: 55,
//             isNew: false,
//             description: "Colorful tin trunk with festive patterns. Reusable and durable."
//         },
//         {
//             id: 7,
//             name: "Fabric Covered Box",
//             type: "Standard Box",
//             occasion: "Wedding",
//             material: "Fabric",
//             sizes: ["Large"],
//             prices: { "Large": 3000 },
//             image: "https://placehold.co/400x400/6f42c1/fff?text=Fabric+Box",
//             inStock: true,
//             stockCount: 5, // Low stock
//             rating: 4.9,
//             reviews: 10,
//             isNew: true,
//             description: "Premium box covered in velvet fabric. The ultimate luxury choice."
//         },
//         {
//             id: 8,
//             name: "Kraft Paper Box",
//             type: "Standard Box",
//             occasion: "Thank You",
//             material: "Cardboard",
//             sizes: ["Small", "Medium", "Large"],
//             prices: { "Small": 500, "Medium": 800, "Large": 1100 },
//             image: "https://placehold.co/400x400/a1887f/fff?text=Kraft+Box",
//             inStock: true,
//             stockCount: 100,
//             rating: 4.3,
//             reviews: 200,
//             isNew: false,
//             description: "Eco-friendly kraft paper box. Simple and sustainable."
//         }
//     ];

//     // --- State ---
//     let state = {
//         filters: {
//             search: '',
//             types: [],
//             occasions: [],
//             sizes: [],
//             materials: [],
//             maxPrice: 10000,
//             inStockOnly: true
//         },
//         sort: 'newest',
//         view: 'grid',
//         itemsPerPage: 12
//     };

//     // --- DOM Elements ---
//     const gridContainer = document.getElementById('products-grid');
//     const resultsCount = document.getElementById('results-count');
//     const emptyState = document.getElementById('empty-state');
//     const loadMoreContainer = document.getElementById('load-more-container');

//     // Filters
//     const desktopSearch = document.getElementById('desktop-search-input');
//     const mobileSearch = document.getElementById('mobile-search-input');
//     const typeFiltersContainer = document.getElementById('type-filters');
//     const occasionFiltersContainer = document.getElementById('occasion-filters');
//     const sizeFiltersContainer = document.getElementById('size-filters');
//     const materialFiltersContainer = document.getElementById('material-filters');
//     const priceRange = document.getElementById('priceRange');
//     const priceValue = document.getElementById('priceValue');
//     const inStockCheckbox = document.getElementById('inStockOnly');
//     const activeFiltersContainer = document.getElementById('active-filters-container');
//     const clearAllBtn = document.getElementById('clear-all-filters');
//     const mobileClearBtn = document.getElementById('mobile-clear-filters');
//     const resetFiltersBtn = document.getElementById('reset-filters-btn');

//     // Sort & View
//     const sortSelect = document.getElementById('sortSelect');
//     const viewGridBtn = document.getElementById('viewGrid');
//     const viewListBtn = document.getElementById('viewList');

//     // --- Initialization ---
//     function init() {
//         renderFilters(document.querySelector('.col-lg-3 .card-body'));
//         setupMobileFilters();
//         applyFilters();
//         setupEventListeners();
//     }

//     function setupMobileFilters() {
//         const desktopFilters = document.querySelector('.col-lg-3 .card-body');
//         const mobileContainer = document.getElementById('mobile-filter-container');
//         if (desktopFilters && mobileContainer) {
//             mobileContainer.innerHTML = desktopFilters.innerHTML;
//         }
//     }

//     // --- Rendering Functions ---

//     function renderFilters(container) {
//         if (!container) return;

//         // Helper to render checkbox list
//         const renderCheckboxList = (items, containerId, filterType) => {
//             const target = container.querySelector(`#${containerId}`);
//             if (!target) return;

//             // Count items
//             const counts = boxes.reduce((acc, item) => {
//                 const val = filterType === 'sizes' ? item.sizes : [item[filterType]]; // Handle array vs string
//                 val.forEach(v => acc[v] = (acc[v] || 0) + 1);
//                 return acc;
//             }, {});

//             const uniqueItems = Object.keys(counts).sort();

//             target.innerHTML = uniqueItems.map(item => `
//                 <div class="form-check mb-2">
//                     <input class="form-check-input ${filterType}-filter" type="checkbox" value="${item}" id="${filterType}-${item}-${container === document.querySelector('.col-lg-3 .card-body') ? 'd' : 'm'}">
//                     <label class="form-check-label d-flex justify-content-between" for="${filterType}-${item}-${container === document.querySelector('.col-lg-3 .card-body') ? 'd' : 'm'}">
//                         <span>${item}</span>
//                         <span class="text-muted small">(${counts[item]})</span>
//                     </label>
//                 </div>
//             `).join('');
//         };

//         // renderCheckboxList(boxes, 'type-filters', 'type');
//         // renderCheckboxList(boxes, 'occasion-filters', 'occasion');
//         // renderCheckboxList(boxes, 'size-filters', 'sizes'); // Special handling in helper
//         renderCheckboxList(boxes, 'material-filters', 'material');
//     }

//     function renderProducts(products) {
//         gridContainer.innerHTML = '';

//         if (products.length === 0) {
//             gridContainer.classList.add('d-none');
//             emptyState.classList.remove('d-none');
//             loadMoreContainer.classList.add('d-none');
//             resultsCount.textContent = 0;
//             return;
//         }

//         gridContainer.classList.remove('d-none');
//         emptyState.classList.add('d-none');
//         resultsCount.textContent = products.length;
//         loadMoreContainer.classList.toggle('d-none', products.length <= state.itemsPerPage);

//         let delay = 0;

//         products.forEach(product => {
//             const colClass = state.view === 'grid' ? 'col-12 col-md-6 col-lg-4' : 'col-12';
//             const cardClass = state.view === 'grid' ? '' : 'list-view';

//             // Badges
//             let badgesHtml = '';
//             if (!product.inStock) {
//                 badgesHtml += `<span class="badge bg-secondary">Out of Stock</span>`;
//             } else if (product.stockCount < 10) {
//                 badgesHtml += `<span class="badge bg-warning text-dark">Limited Stock</span>`;
//             } else if (product.isNew) {
//                 badgesHtml += `<span class="badge bg-primary">New Arrival</span>`;
//             }

//             // Price
//             const minPrice = Math.min(...Object.values(product.prices));

//             const card = document.createElement('div');
//             card.className = colClass;
//             card.setAttribute('data-aos', 'fade-up');
//             card.setAttribute('data-aos-delay', delay);
//             delay += 50;

//             card.innerHTML = `
//                 <div class="box-card ${cardClass}">
//                     <div class="box-image-wrapper">
//                         <div class="badge-overlay">
//                             ${badgesHtml}
//                         </div>
//                         <div class="wishlist-icon" data-id="${product.id}">
//                             <i class="far fa-heart"></i>
//                         </div>
//                         <img src="${product.image}" class="box-image" alt="${product.name}">
//                     </div>
//                     <div class="box-card-body">
//                         <div class="box-badges">
//                             <span class="box-badge">${product.type}</span>
//                             <span class="box-badge" style="background-color: #fff0f3; color: #d63384; border-color: #fcc2d7;">${product.occasion}</span>
//                         </div>
//                         <h5 class="fw-bold mb-2 text-truncate">${product.name}</h5>
                        
//                         <div class="box-details">
//                             <div class="mb-1"><i class="fas fa-ruler-combined"></i> ${product.sizes.join(', ')}</div>
//                             <div><i class="fas fa-layer-group"></i> ${product.material}</div>
//                         </div>

//                         <div class="box-price-section">
//                             <div class="d-flex justify-content-between align-items-end mb-3">
//                                 <div>
//                                     <small class="text-muted d-block" style="font-size: 0.75rem;">Starting from</small>
//                                     <span class="fw-bold text-primary fs-5">₹${minPrice}</span>
//                                 </div>
//                                 <div class="text-warning small">
//                                     <i class="fas fa-star"></i> ${product.rating}
//                                 </div>
//                             </div>
//                             <button class="choose-btn" data-id="${product.id}" ${!product.inStock ? 'disabled style="background:#ccc;"' : ''}>
//                                 ${product.inStock ? 'Choose This Box' : 'Out of Stock'}
//                             </button>
//                             <a class="quick-view-link" data-id="${product.id}">Quick View</a>
//                         </div>
//                     </div>
//                 </div>
//             `;
//             gridContainer.appendChild(card);
//         });
//     }

//     function renderActiveFilters() {
//         activeFiltersContainer.innerHTML = '';

//         if (state.filters.search) addActiveFilterTag(`Search: "${state.filters.search}"`, () => { state.filters.search = ''; desktopSearch.value = ''; mobileSearch.value = ''; applyFilters(); });

//         state.filters.types.forEach(val => addActiveFilterTag(val, () => { state.filters.types = state.filters.types.filter(t => t !== val); document.querySelectorAll(`.type-filter[value="${val}"]`).forEach(el => el.checked = false); applyFilters(); }));
//         state.filters.occasions.forEach(val => addActiveFilterTag(val, () => { state.filters.occasions = state.filters.occasions.filter(t => t !== val); document.querySelectorAll(`.occasion-filter[value="${val}"]`).forEach(el => el.checked = false); applyFilters(); }));
//         state.filters.sizes.forEach(val => addActiveFilterTag(val, () => { state.filters.sizes = state.filters.sizes.filter(t => t !== val); document.querySelectorAll(`.sizes-filter[value="${val}"]`).forEach(el => el.checked = false); applyFilters(); }));
//         state.filters.materials.forEach(val => addActiveFilterTag(val, () => { state.filters.materials = state.filters.materials.filter(t => t !== val); document.querySelectorAll(`.material-filter[value="${val}"]`).forEach(el => el.checked = false); applyFilters(); }));

//         if (state.filters.maxPrice < 10000) addActiveFilterTag(`Max Price: ₹${state.filters.maxPrice}`, () => { state.filters.maxPrice = 10000; document.querySelectorAll('#priceRange').forEach(el => el.value = 10000); document.querySelectorAll('#priceValue').forEach(el => el.textContent = 10000); applyFilters(); });
//     }

//     function addActiveFilterTag(text, removeCallback) {
//         const tag = document.createElement('div');
//         tag.className = 'active-filter-tag';
//         tag.innerHTML = `<span>${text}</span> <i class="fas fa-times"></i>`;
//         tag.querySelector('i').addEventListener('click', removeCallback);
//         activeFiltersContainer.appendChild(tag);
//     }

//     // --- Logic Functions ---

//     function applyFilters() {
//         let filtered = boxes.filter(item => {
//             if (state.filters.search && !item.name.toLowerCase().includes(state.filters.search.toLowerCase())) return false;
//             if (state.filters.types.length > 0 && !state.filters.types.includes(item.type)) return false;
//             if (state.filters.occasions.length > 0 && !state.filters.occasions.includes(item.occasion)) return false;
//             if (state.filters.sizes.length > 0 && !item.sizes.some(s => state.filters.sizes.includes(s))) return false;
//             if (state.filters.materials.length > 0 && !state.filters.materials.includes(item.material)) return false;

//             const minPrice = Math.min(...Object.values(item.prices));
//             if (minPrice > state.filters.maxPrice) return false;

//             if (state.filters.inStockOnly && !item.inStock) return false;

//             return true;
//         });

//         // Sort
//         filtered.sort((a, b) => {
//             const priceA = Math.min(...Object.values(a.prices));
//             const priceB = Math.min(...Object.values(b.prices));

//             switch (state.sort) {
//                 case 'priceLow': return priceA - priceB;
//                 case 'priceHigh': return priceB - priceA;
//                 case 'popular': return b.reviews - a.reviews;
//                 case 'rating': return b.rating - a.rating;
//                 case 'name': return a.name.localeCompare(b.name);
//                 case 'newest': default: return (b.isNew === a.isNew) ? 0 : b.isNew ? 1 : -1;
//             }
//         });




//         renderActiveFilters();

//         // Update mobile badge
//         const activeCount = (state.filters.search ? 1 : 0) + state.filters.types.length + state.filters.occasions.length + state.filters.sizes.length + state.filters.materials.length + (state.filters.maxPrice < 10000 ? 1 : 0);
//         const mobileBadge = document.getElementById('mobile-active-filters-count');
//         if (activeCount > 0) {
//             mobileBadge.textContent = activeCount;
//             mobileBadge.style.display = 'inline-block';
//         } else {
//             mobileBadge.style.display = 'none';
//         }
//     }

//     // --- Event Listeners ---

//     function setupEventListeners() {
//         // Global Delegation
//         document.body.addEventListener('change', (e) => {
//             const handleCheckbox = (filterArrName, value) => {
//                 if (e.target.checked) {
//                     if (!state.filters[filterArrName].includes(value)) state.filters[filterArrName].push(value);
//                 } else {
//                     state.filters[filterArrName] = state.filters[filterArrName].filter(t => t !== value);
//                 }
//                 document.querySelectorAll(`.${filterArrName.slice(0, -1)}-filter[value="${value}"]`).forEach(el => el.checked = e.target.checked); // Sync
//                 applyFilters();
//             };

//             if (e.target.classList.contains('type-filter')) handleCheckbox('types', e.target.value);
//             if (e.target.classList.contains('occasion-filter')) handleCheckbox('occasions', e.target.value);
//             if (e.target.classList.contains('sizes-filter')) handleCheckbox('sizes', e.target.value);
//             if (e.target.classList.contains('material-filter')) handleCheckbox('materials', e.target.value);

//             if (e.target.id === 'inStockOnly' || e.target.id === 'inStockOnly-mobile') {
//                 state.filters.inStockOnly = e.target.checked;
//                 document.querySelectorAll('#inStockOnly').forEach(el => el.checked = e.target.checked);
//                 applyFilters();
//             }
//         });

//         // Search
//         const handleSearch = (e) => {
//             state.filters.search = e.target.value;
//             if (e.target === desktopSearch) mobileSearch.value = e.target.value;
//             else desktopSearch.value = e.target.value;
//             applyFilters();
//         };
//         desktopSearch.addEventListener('input', handleSearch);
//         mobileSearch.addEventListener('input', handleSearch);

//         // Price
//         document.body.addEventListener('input', (e) => {
//             if (e.target.classList.contains('form-range') && e.target.id === 'priceRange') {
//                 const val = e.target.value;
//                 state.filters.maxPrice = parseInt(val);
//                 document.querySelectorAll('#priceValue').forEach(el => el.textContent = val);
//                 document.querySelectorAll('#priceRange').forEach(el => el.value = val);
//                 applyFilters();
//             }
//         });

//         // Clear All
//         const clearAll = (e) => {
//             e.preventDefault();
//             state.filters = { search: '', types: [], occasions: [], sizes: [], materials: [], maxPrice: 10000, inStockOnly: false };

//             desktopSearch.value = ''; mobileSearch.value = '';
//             document.querySelectorAll('input[type="checkbox"]').forEach(el => el.checked = false);
//             document.querySelectorAll('#priceRange').forEach(el => el.value = 10000);
//             document.querySelectorAll('#priceValue').forEach(el => el.textContent = 10000);

//             applyFilters();
//         };
//         clearAllBtn.addEventListener('click', clearAll);
//         mobileClearBtn.addEventListener('click', clearAll);
//         resetFiltersBtn.addEventListener('click', clearAll);

//         // Sort & View
//         sortSelect.addEventListener('change', (e) => { state.sort = e.target.value; applyFilters(); });
//         viewGridBtn.addEventListener('click', () => { state.view = 'grid'; viewGridBtn.classList.add('active'); viewListBtn.classList.remove('active'); applyFilters(); });
//         viewListBtn.addEventListener('click', () => { state.view = 'list'; viewListBtn.classList.add('active'); viewGridBtn.classList.remove('active'); applyFilters(); });

//         // Card Actions
//         gridContainer.addEventListener('click', (e) => {
//             // Wishlist
//             const wishlistBtn = e.target.closest('.wishlist-icon');
//             if (wishlistBtn) {
//                 const icon = wishlistBtn.querySelector('i');
//                 icon.classList.toggle('far');
//                 icon.classList.toggle('fas');
//                 icon.classList.toggle('text-danger');

//                 anime({ targets: wishlistBtn, scale: [1, 1.4, 1], duration: 400, easing: 'easeOutQuad' });

//                 const countBadge = document.getElementById('wishlist-count');
//                 let count = parseInt(countBadge.textContent);
//                 if (icon.classList.contains('fas')) { count++; countBadge.style.display = 'block'; }
//                 else { count--; if (count === 0) countBadge.style.display = 'none'; }
//                 countBadge.textContent = count;
//                 return;
//             }

//             // Choose / Quick View
//             const id = e.target.dataset.id;
//             if (!id) return;
//             const product = boxes.find(p => p.id == id);

//             if (e.target.classList.contains('choose-btn')) {
//                 // Select Box Logic
//                 // For now, just show sticky bar with selection
//                 showStickyBar(product);
//             } else if (e.target.classList.contains('quick-view-link')) {
//                 openQuickView(product);
//             }
//         });
//     }

//     // --- Quick View & Sticky Bar ---
//     const quickViewModal = new bootstrap.Modal(document.getElementById('quickViewModal'));

//     function openQuickView(product) {
//         document.getElementById('qv-img').src = product.image;
//         document.getElementById('qv-title').textContent = product.name;
//         document.getElementById('qv-type').textContent = product.type;
//         document.getElementById('qv-occasion').textContent = product.occasion;
//         document.getElementById('qv-desc').textContent = product.description;
//         document.getElementById('qv-reviews').textContent = `(${product.reviews} reviews)`;

//         // Rating
//         let stars = '';
//         for (let i = 1; i <= 5; i++) {
//             if (i <= product.rating) stars += '<i class="fas fa-star"></i>';
//             else if (i - 0.5 <= product.rating) stars += '<i class="fas fa-star-half-alt"></i>';
//             else stars += '<i class="far fa-star"></i>';
//         }
//         document.getElementById('qv-rating').innerHTML = stars;

//         // Sizes
//         const sizesContainer = document.getElementById('qv-sizes');
//         sizesContainer.innerHTML = product.sizes.map(size => `
//             <div class="size-option-row d-flex justify-content-between align-items-center" onclick="selectSize(this, ${product.prices[size]})">
//                 <span class="fw-bold">${size}</span>
//                 <span>₹${product.prices[size]}</span>
//             </div>
//         `).join('');

//         // Default Price
//         const minPrice = Math.min(...Object.values(product.prices));
//         document.getElementById('qv-price').textContent = `₹${minPrice}`;

//         // Add Button
//         const addBtn = document.getElementById('qv-add-btn');
//         addBtn.onclick = () => {
//             quickViewModal.hide();
//             showStickyBar(product);
//         };

//         quickViewModal.show();
//     }

//     window.selectSize = function (el, price) {
//         document.querySelectorAll('.size-option-row').forEach(e => e.classList.remove('selected'));
//         el.classList.add('selected');
//         document.getElementById('qv-price').textContent = `₹${price}`;
//     };

//     function showStickyBar(product) {
//         const bar = document.getElementById('sticky-bottom-bar');
//         document.getElementById('sticky-box-img').src = product.image;
//         document.getElementById('sticky-box-name').textContent = product.name;

//         const minPrice = Math.min(...Object.values(product.prices));
//         document.getElementById('sticky-box-price').textContent = `Starting from ₹${minPrice}`;

//         bar.classList.remove('d-none');
//         bar.classList.add('d-block', 'animate__animated', 'animate__slideInUp');
//     }

//     // Initialize
//     init();
// });
