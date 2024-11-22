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
        this.dropdown = document.querySelector("#" + this.element.dataset.toggles);
        this.element.addEventListener("click", this.click.bind(this));
    }

    close() {
        this.element.classList.remove("header__nav-item--dropdown-open");
        this.dropdown.classList.remove("header__dropdown--open");
    }

    open() {
        this.element.classList.add("header__nav-item--dropdown-open");
        this.dropdown.classList.add("header__dropdown--open");
    }

    click(event) {
        event.preventDefault();
        let open = this.element.classList.contains("header__nav-item--dropdown-open");
        window.dropdowns.forEach(function(dropdown) {
            dropdown.close();
        });
        if (!open) {
            this.open();
        }
        return false;
    }
}

class ThemeSwitcher {
    constructor(element) {
        this.element = element;
        this.body = document.querySelector("body");
        this.browserDark = window.matchMedia("(prefers-color-scheme: dark)");
        this.element.addEventListener("click", this.click.bind(this));
    }

    setCookie(theme) {
        const date = new Date();
        date.setFullYear(date.getFullYear() + 1);
        document.cookie = "theme=" + theme + "; expires=" + date.toUTCString() + "; path=/";
    }

    setLight() {
        this.body.dataset.theme = "light";
        this.setCookie("light");
    }

    setDark() {
        this.body.dataset.theme = "dark";
        this.setCookie("dark");
    }

    click() {
        if (!this.body.hasAttribute("data-theme")) {
            if (this.browserDark) {
                this.setLight();
            } else {
                this.setDark();
            }
        } else if (this.body.dataset.theme === "light") {
            this.setDark();
        } else {
            this.setLight();
        }
    }
}

window.addEventListener("load", function() {
    window.dropdowns = [];
    window.autoSlugs = [];
    // dropdown toggles
    document.querySelectorAll("[data-toggles]").forEach(function(dropdown) {
        window.dropdowns.push(new DropdownMenu(dropdown));
    });
    // auto slug
    document.querySelectorAll("form[data-auto-slug][data-auto-slug-from]").forEach(function(autoSlugForm) {
        window.autoSlugs.push(new AutoSlug(autoSlugForm));
    });
    // theme switcher
    window.themeSwitcher = new ThemeSwitcher(document.querySelector(".theme-switcher"));
});
