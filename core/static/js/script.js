// Function to show/hide nav menu (hamburger toggle)
const showMenu = (toggleId, navId) => {
  const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId);

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('show-menu');
      toggle.classList.toggle('show-icon');
    });
  }
};

showMenu('nav-toggle', 'nav-menu');

// Function to toggle dropdown on click
const dropdownItems = document.querySelectorAll('.dropdown__item');

dropdownItems.forEach(item => {
  item.addEventListener('click', function (e) {
    e.stopPropagation();

    const dropdownMenu = this.querySelector('.dropdown__menu');

    document.querySelectorAll('.dropdown__menu').forEach(menu => {
      if (menu !== dropdownMenu) {
        menu.style.maxHeight = null;
      }
    });

    if (dropdownMenu.style.maxHeight) {
      dropdownMenu.style.maxHeight = null;
    } else {
      dropdownMenu.style.maxHeight = dropdownMenu.scrollHeight + "px";
    }
  });
});

// Close dropdowns if clicked outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.dropdown__item')) {
    document.querySelectorAll('.dropdown__menu').forEach(menu => {
      menu.style.maxHeight = null;
    });
  }
});

// Initialize Swiper
var swiper = new Swiper(".team-swiper", {
  navigation: {
    nextEl: ".swiper-button-nexts",
    prevEl: ".swiper-button-prevs",
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  loop: true,
  slidesPerView: 1,
  spaceBetween: 10,
  breakpoints: {
    250: {
      slidesPerView: 1.2,
      spaceBetween: 80
    },
    300: {
      slidesPerView: 1.2,
      spaceBetween: 0
    },
    400: {
      slidesPerView: 1.5,
      spaceBetween: 20
    },
    640: {
      slidesPerView: 2,
      spaceBetween: 40
    },
    840: {
      slidesPerView: 3,
      spaceBetween: 40
    },
    1150: {
      slidesPerView: 4,
      spaceBetween: 40
    }
  }
});
