document.addEventListener('DOMContentLoaded', function () {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');
  const mobileOverlay = document.getElementById('mobileOverlay');

  // Initialize submenu classes
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(function (item) {
    const submenu = item.querySelector('.nav-submenu');
    if (submenu) {
      item.classList.add('has-submenu');
    }
  });
  // Sidebar toggle functionality
  sidebarToggle.addEventListener('click', function () {
    if (window.innerWidth <= 768) {
      sidebar.classList.toggle('show');
      mobileOverlay.classList.toggle('show');
    } else {
      sidebar.classList.toggle('collapsed');
      mainContent.classList.toggle('expanded');
    }
  });

  mobileOverlay.addEventListener('click', function () {
    sidebar.classList.remove('show');
    mobileOverlay.classList.remove('show');
  });

  // Navigation links functionality
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();

      const parentItem = link.closest('.nav-item');
      const submenu = parentItem
        ? parentItem.querySelector('.nav-submenu')
        : null;

      // Handle submenu toggle
      if (submenu) {
        const isOpen = parentItem.classList.contains('open');

        // Close all other submenus
        document
          .querySelectorAll('.nav-item.open')
          .forEach(function (openItem) {
            if (openItem !== parentItem) {
              openItem.classList.remove('open');
              const otherSubmenu = openItem.querySelector('.nav-submenu');
              if (otherSubmenu) {
                otherSubmenu.classList.remove('show');
              }
            }
          });

        // Toggle current submenu
        if (isOpen) {
          parentItem.classList.remove('open');
          submenu.classList.remove('show');
        } else {
          parentItem.classList.add('open');
          submenu.classList.add('show');
        }
      }

      // Update active state for main nav links only
      if (!link.classList.contains('nav-link-sub')) {
        navLinks.forEach(function (l) {
          if (!l.classList.contains('nav-link-sub')) {
            l.classList.remove('active');
          }
        });
        link.classList.add('active');

        // Update page title
        // const linkText = link.querySelector("span").textContent;
        // document.getElementById("pageTitle").textContent = "Dashboard " + linkText;
      }
    });
  });

  // Sub navigation links functionality
  const subNavLinks = document.querySelectorAll('.nav-link-sub');
  subNavLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      //e.preventDefault();

      // Remove active state from all sub links
      subNavLinks.forEach(function (l) {
        l.classList.remove('active');
      });

      // Add active state to clicked link
      link.classList.add('active');

      // Update page title with sub navigation
      // const linkText = link.textContent.trim();
      // document.getElementById("pageTitle").textContent = "Dashboard - " + linkText;
    });
  });
});
