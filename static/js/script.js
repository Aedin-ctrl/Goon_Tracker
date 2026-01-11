document.addEventListener('DOMContentLoaded', function () {
    const foodInput = document.getElementById('food');
    const autocompleteList = document.getElementById('autocomplete-list');
    const portionsSelect = document.getElementById('portions');
    const customPortions = document.getElementById('custom-portions');
    const weightInput = document.getElementById('weight');

    const calculateBtn = document.getElementById('calculate');
    const results = document.getElementById('results');
    const caloriesSpan = document.getElementById('calories');
    const proteinSpan = document.getElementById('protein');

    const hiddenCalories = document.getElementById('hidden-calories');
    const hiddenProtein = document.getElementById('hidden-protein');
    const servingDesc = document.getElementById('serving-desc');

    /* ---------- AUTOCOMPLETE ---------- */
    function showItems(items) {
        autocompleteList.innerHTML = '';
        items.forEach(name => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item';
            div.textContent = name;

            div.onclick = () => {
                foodInput.value = name;
                autocompleteList.innerHTML = '';

                // Fetch serving description
                fetch('/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `food=${encodeURIComponent(name)}&portions=1`
                })
                    .then(res => res.json())
                    .then(data => {
                        servingDesc.textContent = data.serving_desc || '';
                    });
            };

            autocompleteList.appendChild(div);
        });
    }

    foodInput.addEventListener('input', function () {
        const query = this.value.trim();

        if (query.length < 2) {
            autocompleteList.innerHTML = '';
            return;
        }

        fetch(`/autocomplete?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(items => showItems(items));
    });

    // NEW FEATURE: Show all foods on focus
    foodInput.addEventListener('focus', function () {
        fetch('/autocomplete?q=') // empty query returns all foods
            .then(res => res.json())
            .then(items => showItems(items));
    });

    /* ---------- PORTIONS ---------- */
    portionsSelect.addEventListener('change', function () {
        if (this.value === 'custom') {
            customPortions.style.display = 'block';
        } else {
            customPortions.style.display = 'none';
            customPortions.value = '';
        }
    });

    /* ---------- CALCULATE ---------- */
    calculateBtn.addEventListener('click', function () {
        const food = foodInput.value.trim();
        if (!food) {
            alert('Please enter a food');
            return;
        }

        let portions = portionsSelect.value;
        let weight = weightInput.value;

        // Portions take priority
        if (portions === 'custom') {
            portions = customPortions.value;
        }

        if (!portions && !weight) {
            alert('Enter portions or weight');
            return;
        }

        const formData = new FormData();
        formData.append('food', food);
        formData.append('portions', portions);
        formData.append('weight', weight);

        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                caloriesSpan.textContent = data.calories;
                proteinSpan.textContent = data.protein;

                hiddenCalories.value = data.calories;
                hiddenProtein.value = data.protein;

                results.style.display = 'block';
            });
    });
});

/* ---------- REQUIRED: GLOBAL FUNCTION ---------- */
window.changePerson = function () {
    const person = document.getElementById('person').value;
    window.location.href = `/?person=${encodeURIComponent(person)}`;
};