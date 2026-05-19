/* Landing page interactions */
(function () {
    var navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-up').forEach(function (el) {
        observer.observe(el);
    });

    var locale = document.body.getAttribute('data-locale') || 'ru';
    var localeMap = { kk: 'kk-KZ', ru: 'ru-RU', en: 'en-US' };
    var countLocale = localeMap[locale] || 'ru-RU';

    var statsObserved = false;
    var statsObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting || statsObserved) return;
            statsObserved = true;
            document.querySelectorAll('.stat-val[data-count]').forEach(function (el) {
                var target = parseInt(el.getAttribute('data-count'), 10);
                var duration = 1500;
                var startTime = null;
                function animate(timestamp) {
                    if (!startTime) startTime = timestamp;
                    var progress = Math.min((timestamp - startTime) / duration, 1);
                    var eased = 1 - Math.pow(1 - progress, 3);
                    el.textContent = Math.floor(eased * target).toLocaleString(countLocale) + '+';
                    if (progress < 1) requestAnimationFrame(animate);
                }
                requestAnimationFrame(animate);
            });
        });
    }, { threshold: 0.3 });

    var statsSection = document.querySelector('.stats-lp');
    if (statsSection) statsObserver.observe(statsSection);

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var href = this.getAttribute('href');
            if (href.length <= 1) return;
            e.preventDefault();
            var target = document.querySelector(href);
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            var menu = document.getElementById('mobileMenu');
            if (menu) menu.classList.add('d-none');
        });
    });
})();
