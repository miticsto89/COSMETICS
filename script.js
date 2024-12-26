document.addEventListener('DOMContentLoaded', () => {
    const API_KEY = '107a1219-96c01308-f4569489-336df56e';
    const API_URL = 'https://fortniteapi.io/v2/shop?lang=es';

    fetch(API_URL, {
        headers: {
            'Authorization': API_KEY
        }
    })
    .then(response => response.json())
    .then(data => {
        const shopContainer = document.getElementById('shop');
        const sortedData = data.shop.sort((a, b) => new Date(a.offerDates.out) - new Date(b.offerDates.out));

        sortedData.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.classList.add('item');

            const img = document.createElement('img');
            img.src = item.displayAssets[0].full_background;
            img.alt = item.displayName;

            const itemInfo = document.createElement('div');
            itemInfo.classList.add('item-info');

            const title = document.createElement('h3');
            title.textContent = item.displayName;

            const price = document.createElement('p');
            const price_usd = ((item.price.finalPrice * 0.46) / 100) - 0.25;
            price.textContent = `Precio (USD): $${price_usd.toFixed(2)}`;

            itemInfo.appendChild(title);
            itemInfo.appendChild(price);
            itemElement.appendChild(img);
            itemElement.appendChild(itemInfo);
            
            itemElement.addEventListener('click', () => {
                alert(`Más información sobre ${item.displayName}`);
            });

            shopContainer.appendChild(itemElement);
        });
    })
    .catch(error => console.error('Error:', error));
});
