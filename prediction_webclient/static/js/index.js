Vue.component('tooltip-icon', {
    props: ["title"],
    template: `
    <span data-toggle="tooltip" data-placement="auto" :title="title">
    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
        <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"/>
    </svg>
    </span>
    `
})

var app = new Vue({
    el: '#app',
    data: {
        form: {
            state: null,
            county: null,
            age: null,
            metal_levels: null,
            plan_types: null,
            select_fields: {
                "states": [],
                "counties": [],
                "metal_levels": [],
                "plan_types": []
            }
        },
        tooltips: {
            "metal_levels": "Plans in the Marketplace are presented in 4 “metal” categories: Bronze, Silver, Gold, and Platinum. (“Catastrophic” plans are also available to some people.) Catastrophic health insurance plans have low monthly premiums and very high deductibles. They may be an affordable way to protect yourself from worst-case scenarios, like getting seriously sick or injured. But you pay most routine medical expenses yourself.",
            "plan_types": "There are different types of Marketplace health insurance plans designed to meet different needs. Some types of plans restrict your provider choices or encourage you to get care from the plan’s network of doctors, hospitals, pharmacies, and other medical service providers. Others pay a greater share of costs for providers outside the plan’s network."
        },
        predictions: null,
        error: null,
        loading: false
    },
    methods: {
        init: async function() {
            let response = await fetch('/vue/form');
            let data = await response.json();
            this.form = data;
        },
        refreshCounties: async function() {
            let response = await fetch('/vue/counties?state=' + this.form.state)
            let data = await response.json();
            this.form.select_fields['counties'] = data.counties;
            this.form.county = this.form.select_fields.counties[0]['value'];
        },
        submit_form: async function() {

            // Create a deep copy of form
            let form = Object.assign({}, this.form);

            // Delete select_fields to save bandwidth
            delete form['select_fields'];

            // Convert data types
            form['age'] = parseInt(form['age'])
            form['smoker'] = (form['smoker'] == "true")

            // Set loading state to true (spinner)
            this.loading = true;

            let response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(form)
            })

            let data = await response.json();

            if ("error" in data) {
                this.error = data["error"];
                this.predictions = null
            } else {
                // Remove old error
                this.error = null;
                this.predictions = data;
            }

            // Set loading state to false (spinner)
            this.loading = false;

            // Show modal
            new bootstrap.Modal(document.getElementById('modal')).show()
        },
        formatCurrency: function(value) {
            // Create number formatter.
            var formatter = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2
            });

            return formatter.format(value);
        }
    }
});

app.init();

$('document').ready(() => {
    $('[data-toggle="tooltip"]').tooltip();
});