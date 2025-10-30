document.addEventListener("DOMContentLoaded", () => {
  const menuContainer = document.querySelector(".menu");

  fetch("/static/menu.json")
    .then(res => res.json())
    .then(drinks => {
      const grouped = groupByCategory(drinks);

      for (const [category, items] of Object.entries(grouped)) {
        const section = document.createElement("div");
        section.className = "category";

        const title = document.createElement("h2");
        title.textContent = category;
        section.appendChild(title);

        const grid = document.createElement("div");
        grid.className = "drinks-grid";

        items.forEach(d => {
          const card = document.createElement("div");
          card.className = "drink-card";
          card.innerHTML = `
            <img src="${d.image}" alt="${d.name}" />
            <h3>${d.name}</h3>
            <p>€${Number(d.price).toFixed(2)}</p>
            <button onclick="orderDrink('${d.name.replace(/'/g, "\\'")}', ${Number(d.price)})">Добавить</button>
          `;
          grid.appendChild(card);
        });

        section.appendChild(grid);
        menuContainer.appendChild(section);
      }
    })
    .catch(err => console.error("Ошибка загрузки меню:", err));
});

function groupByCategory(drinks) {
  return drinks.reduce((acc, drink) => {
    (acc[drink.category] = acc[drink.category] || []).push(drink);
    return acc;
  }, {});
}

function orderDrink(name, price) {
  if (window.Telegram && Telegram.WebApp) {
    Telegram.WebApp.sendData(JSON.stringify({ action: "order", name, price }));
  }
  alert(`Вы выбрали ${name} (€${price.toFixed(2)})`);
}

