/* =====================================================
   INTERNSHIP MANAGEMENT SYSTEM — Main JavaScript
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ---- Sidebar Mobile Toggle ----
    const mobileToggle = document.querySelector('.mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');

    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });

        // Close sidebar when clicking outside on mobile
        if (mainContent) {
            mainContent.addEventListener('click', function () {
                if (sidebar.classList.contains('open')) {
                    sidebar.classList.remove('open');
                }
            });
        }
    }

    // ---- Auto-dismiss alerts ----
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        // Auto-dismiss after 5 seconds
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                alert.remove();
            }, 300);
        }, 5000);

        // Manual dismiss
        const dismissBtn = alert.querySelector('.alert-dismiss');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', function () {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                setTimeout(function () {
                    alert.remove();
                }, 300);
            });
        }
    });

    // ---- Confirmation Dialogs ----
    const confirmForms = document.querySelectorAll('[data-confirm]');
    confirmForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const message = form.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ---- Dynamic Search Filter for Tables ----
    const searchInputs = document.querySelectorAll('[data-table-search]');
    searchInputs.forEach(function (input) {
        const tableId = input.getAttribute('data-table-search');
        const table = document.getElementById(tableId);

        if (table) {
            input.addEventListener('input', function () {
                const filter = input.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');

                rows.forEach(function (row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                });
            });
        }
    });

    // ---- Active Sidebar Link ----
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-link');

    sidebarLinks.forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });

    // ---- Progress Bar Animation ----
    const progressFills = document.querySelectorAll('.progress-fill');
    progressFills.forEach(function (fill) {
        const width = fill.getAttribute('data-width') || fill.style.width;
        fill.style.width = '0%';
        setTimeout(function () {
            fill.style.width = width;
        }, 200);
    });

    // ---- Cover Letter Toggle ----
    const coverLetterToggles = document.querySelectorAll('.toggle-cover-letter');
    coverLetterToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = toggle.getAttribute('data-target');
            const target = document.getElementById(targetId);
            if (target) {
                target.style.display = target.style.display === 'none' ? 'block' : 'none';
                toggle.textContent = target.style.display === 'none' ? 'Show Cover Letter' : 'Hide Cover Letter';
            }
        });
    });

    // ---- File Input Preview ----
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            const fileName = input.files.length > 0 ? input.files[0].name : 'No file chosen';
            const label = input.closest('.form-group');
            if (label) {
                let preview = label.querySelector('.file-name-preview');
                if (!preview) {
                    preview = document.createElement('span');
                    preview.className = 'file-name-preview text-sm text-muted mt-1';
                    preview.style.display = 'block';
                    input.parentNode.appendChild(preview);
                }
                preview.textContent = fileName;
            }
        });
    });

    // ---- Smooth scroll for anchor links ----
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            const targetId = link.getAttribute('href').slice(1);
            const target = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ---- Animate elements on scroll ----
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animateElements = document.querySelectorAll('.stat-card, .internship-card, .feature-card');
    animateElements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    // ---- Tooltip initialization ----
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(function (el) {
        el.style.position = 'relative';
        el.addEventListener('mouseenter', function () {
            const tip = document.createElement('div');
            tip.className = 'tooltip-popup';
            tip.textContent = el.getAttribute('data-tooltip');
            tip.style.cssText = 'position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:6px 12px;border-radius:6px;font-size:0.75rem;white-space:nowrap;z-index:1000;pointer-events:none;animation:fadeInUp 0.2s ease;';
            el.appendChild(tip);
        });
        el.addEventListener('mouseleave', function () {
            const tip = el.querySelector('.tooltip-popup');
            if (tip) tip.remove();
        });
    });

});
