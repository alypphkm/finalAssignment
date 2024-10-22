const carDetails = {
    'Toyota Highlander': {
        image: 'toyota_highlanders.jpg',
        description: 'A mid-size SUV with a comfortable ride and spacious interior.',
        price: 50 // price per hour
    },
    'Honda Pilot': {
        image: 'honda_pilot.jpg',
        description: 'A versatile SUV with ample seating and cargo space.',
        price: 55
    },
    'Ford Explorer': {
        image: 'ford_explorer.jpg',
        description: 'A powerful SUV with advanced technology and plenty of space.',
        price: 60
    },
    'Volkswagen Golf': {
        image: 'vw_golf.jpg',
        description: 'A compact hatchback with great fuel efficiency and a stylish design.',
        price: 30
    },
    'Honda Fit': {
        image: 'honda_fit.jpg',
        description: 'A small hatchback with a surprisingly spacious interior and agile handling.',
        price: 35
    },
    'Ford Fiesta': {
        image: 'ford_fiesta.jpg',
        description: 'A fun-to-drive hatchback with a modern look and great features.',
        price: 40
    },
    'Toyota Corolla': {
        image: 'toyota_corolla.jpg',
        description: 'A reliable sedan with excellent fuel economy and a comfortable interior.',
        price: 25
    },
    'Honda Accord': {
        image: 'honda_accord.jpg',
        description: 'A midsize sedan with a spacious cabin, powerful engines, and modern technology.',
        price: 30
    },
    'Nissan Altima': {
        image: 'nissan_altima.jpg',
        description: 'A stylish sedan with a comfortable ride and advanced safety features.',
        price: 28
    },
    'Chevrolet Camaro': {
        image: 'chevrolet_camaro.jpg',
        description: 'A high-performance sportscar with a sleek design and powerful engines.',
        price: 70
    },
    'Ford Mustang': {
        image: 'ford_mustang.jpg',
        description: 'An iconic sportscar known for its powerful performance and bold style.',
        price: 75
    },
    'Porsche 911': {
        image: 'porsche_911.jpg',
        description: 'A luxury sportscar with exceptional handling and a high-performance engine.',
        price: 100
    }
};

function selectCarType(carType) {
    document.getElementById('carType').value = carType;

    const carModels = {
        'SUV': ['Toyota Highlander', 'Honda Pilot', 'Ford Explorer'],
        'Hatchback': ['Volkswagen Golf', 'Honda Fit', 'Ford Fiesta'],
        'Sedan': ['Toyota Corolla', 'Honda Accord', 'Nissan Altima'],
        'Sportcar': ['Chevrolet Camaro', 'Ford Mustang', 'Porsche 911']
    };

    const carModelSelect = document.getElementById('carModel');
    carModelSelect.innerHTML = '<option value="" disabled selected>Select a Car Model</option>';

    if (carModels[carType]) {
        carModels[carType].forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            carModelSelect.appendChild(option);
        });
    }

    carModelSelect.onchange = function () {
        const selectedModel = carModelSelect.value;
        const carImage = document.getElementById('selectedCarImage');
        const carDescription = document.getElementById('carDescription');
        const carPrice = document.getElementById('carPrice');

        if (carDetails[selectedModel]) {
            carImage.src = carDetails[selectedModel].image;
            carImage.style.display = 'block';
            carDescription.textContent = carDetails[selectedModel].description;
            carPrice.textContent = `Price per day: $${carDetails[selectedModel].price}`;
        } else {
            carImage.style.display = 'none';
            carDescription.textContent = '';
            carPrice.textContent = '';
        }
    };
}

function addToCart() {
    const carType = document.getElementById('carType').value;
    const carModel = document.getElementById('carModel').value;
    const bookingDate = document.getElementById('bookingDate').value;
    const bookingTime = document.getElementById('bookingTime').value;
    const bookingLime= document.getElementById('bookingLime').value;
    const pickupLocation = document.getElementById('pickupLocation').value;

    if (!carType || !carModel || !bookingDate || !bookingTime || !pickupLocation) {
        alert('Please fill out all booking details.');
        return;
    }

    const carPrice = carDetails[carModel].price;
    const totalPriceForBooking = carPrice * bookingTime;

    const cartItems = document.getElementById('cartItems');
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>${carType}</td>
        <td>${carModel}</td>
        <td>${bookingDate}</td>
        <td>${bookingTime} day(s)</td>
        <td>${bookingLime}</td>
        <td>${pickupLocation}</td>
        <td>$${totalPriceForBooking}</td>
        <td><button class="remove-btn" onclick="removeItem(this)">Remove</button></td>f
    `;

    cartItems.appendChild(row);


    updateTotalPrice();

    // Clear the form after adding to cart
    document.getElementById('bookingForm').reset();
    document.getElementById('selectedCarImage').style.display = 'none';
    document.getElementById('carDescription').textContent = '';
    document.getElementById('carPrice').textContent = '';


    showNotification('Item added to cart');
}
function saveCartToLocalStorage() {
    const cartItems = document.getElementById('cartItems').innerHTML;
    localStorage.setItem('cartItems', cartItems);
}

function showNotification(message) {
    alert(message);
}

function removeItem(button) {
    const row = button.parentNode.parentNode;
    row.remove();
    updateTotalPrice();
    
    // Save updated cart data to localStorage after removal
    saveCartToLocalStorage();

    showNotification('Item removed from cart');
}

function updateTotalPrice() {
    const cartItems = document.getElementById('cartItems').children;
    let total = 0;

    for (const item of cartItems) {
        const priceCell = item.cells[6];
        const price = parseFloat(priceCell.textContent.replace('$', ''));
        total += price;
    }

    document.getElementById('totalPrice').textContent = total;
}

document.addEventListener('DOMContentLoaded', () => {
    // Retrieve cart items from localStorage
    const savedCartItems = localStorage.getItem('cartItems');
    if (savedCartItems) {
        document.getElementById('cartItems').innerHTML = savedCartItems;
        updateTotalPrice();
    }

    const carModelSelect = document.getElementById('carModel');
    carModelSelect.addEventListener('change', function () {
        const selectedModel = carModelSelect.value;
        const carImage = document.getElementById('selectedCarImage');
        const carDescription = document.getElementById('carDescription');
        const carPrice = document.getElementById('carPrice');

        if (carDetails[selectedModel]) {
            carImage.src = carDetails[selectedModel].image;
            carImage.style.display = 'block';
            carDescription.textContent = carDetails[selectedModel].description;
            carPrice.textContent = `Price per hour: $${carDetails[selectedModel].price}`;
        } else {
            carImage.style.display = 'none';
            carDescription.textContent = '';
            carPrice.textContent = '';
        }
    });
});

window.addEventListener('beforeunload', () => {
    // Save cart items to localStorage before leaving or refreshing the page
    saveCartToLocalStorage();    
});

