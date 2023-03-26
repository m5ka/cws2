const SLUGIFY_FROM = "ÁÄÂÀÃÅČÇĆĎÉĚËÈÊẼĔȆÍÌÎÏŇÑÓÖÒÔÕØŘŔŠŤÚŮÜÙÛÝŸŽáäâàãåčçćďéěëèêẽĕȇíìîïňñóöòôõøðřŕšťúůüùûýÿžĐđÆa·/_,:;";
const SLUGIFY_TO   = "AAAAAACCCDEEEEEEEEIIIINNOOOOOORRSTUUUUUYYZaaaaaacccdeeeeeeeeiiiinnooooooorrstuuuuuyyzDdAa------";

class AutoSlug {
    constructor(formElement) {
        this.form = formElement;
        this.slugFrom = document.querySelector('[name="' + this.form.dataset.autoSlugFrom + '"]');
        this.slugTo = document.querySelector('[name="' + this.form.dataset.autoSlug + '"]');
        if (this.slugTo && this.slugFrom) {
            this.slugFrom.addEventListener("input", this.onInput.bind(this));
            this.onInput();
        }
    }

    onInput() {
        let value = this.slugFrom.value;
        if (value && value.length > 0)
            this.slugTo.placeholder = this.slugify(this.slugFrom.value);
        else
            this.slugTo.placeholder = "";
    }

    slugify(str) {
        str = str.replace(/^\s+|\s+$/g, '').toLowerCase();
        for (let i = 0, l = SLUGIFY_FROM.length; i < l; i++) {
            str = str.replace(new RegExp(SLUGIFY_FROM.charAt(i), 'g'), SLUGIFY_TO.charAt(i));
        }
        str = str.replace(/[^a-z0-9 -]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
        return str;
    }
}

class DropdownMenu {
    constructor(element) {
        this.element = element;
        this.element.querySelector(".dropdown-toggle").addEventListener("click", this.click.bind(this));
    }

    close() {
        this.element.classList.remove("open");
    }

    open() {
        this.element.classList.add("open");
    }

    click(event) {
        event.preventDefault();
        let open = this.element.classList.contains("open");
        window.dropdowns.forEach(function(dropdown) {
            dropdown.close();
        });
        if (!open) {
            this.open();
        }
        return false;
    }
}

window.addEventListener("load", function() {
    window.dropdowns = [];
    window.autoSlugs = [];
    // dropdown toggles
    document.querySelectorAll(".dropdown").forEach(function(dropdown) {
        window.dropdowns.push(new DropdownMenu(dropdown));
    });
    // auto slug
    document.querySelectorAll("form[data-auto-slug][data-auto-slug-from]").forEach(function(autoSlugForm) {
        window.autoSlugs.push(new AutoSlug(autoSlugForm));
    });
    // mobile menu toggle
    const headerElement = document.querySelector("body>header");
    document.querySelector(".hamburger").addEventListener("click", function(event) {
        event.preventDefault();
        headerElement.classList.toggle("show");
        return false;
    });
});