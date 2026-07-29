/* ==========================================================================
   AURORA INTERNATIONAL SPA — INTERACTIVE LOGIC & ANIMATIONS (VOL ONE 2026)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initHeroVideo();
    initIntroCurtain();
    initNavigation();
    initCategoryFilters();
    initQuickBookingDate();
    initScrollReveal();
    initParticleCanvas();
    initSequentialIconHighlight();
    initSoundscapePlayer();
    updateVoucherPreview();
});

/* --- Force 100% Autoplay for Local Background MP4 Video --- */
function initHeroVideo() {
    const video = document.getElementById('hero-bg-video');
    if (!video) return;

    video.muted = true;
    video.playsInline = true;
    
    const playPromise = video.play();
    if (playPromise !== undefined) {
        playPromise.then(() => {
            console.log('Background MP4 video playing successfully!');
        }).catch(err => {
            console.log('Video autoplay retry on interaction:', err);
            document.addEventListener('touchstart', () => video.play(), { once: true });
            document.addEventListener('click', () => video.play(), { once: true });
        });
    }
}

/* --- Soundscape Audio Player (30s Audio Stream from Pinterest Pin 21603273207964484) --- */
function initSoundscapePlayer() {
    const audio = document.getElementById('spa-soundscape');
    const soundBtn = document.getElementById('sound-toggle-btn');
    if (!audio || !soundBtn) return;

    // Attach click handler to single sound button
    soundBtn.addEventListener('click', () => toggleSoundscape());

    // Auto-enable soundscape on first user click anywhere on page if desired
    const startAudioOnGesture = () => {
        if (audio.paused) {
            audio.play().then(() => {
                soundBtn.classList.add('playing');
                soundBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
            }).catch(e => console.log('Audio autoplay gesture catch:', e));
        }
        document.removeEventListener('click', startAudioOnGesture);
    };

    document.addEventListener('click', startAudioOnGesture, { once: true });
}

function toggleSoundscape() {
    const audio = document.getElementById('spa-soundscape');
    const soundBtn = document.getElementById('sound-toggle-btn');
    if (!audio || !soundBtn) return;

    if (audio.paused) {
        audio.play().then(() => {
            soundBtn.classList.add('playing');
            soundBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
        }).catch(err => {
            console.log('Audio play error:', err);
        });
    } else {
        audio.pause();
        soundBtn.classList.remove('playing');
        soundBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
    }
}

/* --- Luxury Intro Curtain Reveal Animation --- */
function initIntroCurtain() {
    const introCurtain = document.getElementById('intro-curtain');
    if (!introCurtain) return;

    setTimeout(() => {
        introCurtain.classList.add('curtain-raise');
        setTimeout(() => {
            introCurtain.style.display = 'none';
        }, 1300);
    }, 2400);
}

/* --- Interactive Home Bottom Icons (Click Icon to Reveal Text Below) --- */
function selectHomeHighlight(index, title, desc) {
    const btns = document.querySelectorAll('.interactive-icon-btn');
    btns.forEach((b, i) => {
        if (i === index) b.classList.add('active');
        else b.classList.remove('active');
    });

    const display = document.getElementById('highlight-text-display');
    const titleEl = document.getElementById('highlight-title');
    const descEl = document.getElementById('highlight-desc');

    if (!display || !titleEl || !descEl) return;

    display.style.opacity = '0';
    display.style.transform = 'translateY(8px)';

    setTimeout(() => {
        titleEl.innerText = title;
        descEl.innerText = desc;
        display.style.opacity = '1';
        display.style.transform = 'translateY(0)';
    }, 180);
}

/* --- Sequential Highlight Loop for Amenity & Etiquette Icons --- */
function initSequentialIconHighlight() {
    const amenityGrids = document.querySelectorAll('#seq-amenities-grid, #seq-etiquette-grid');
    if (!amenityGrids.length) return;

    amenityGrids.forEach(grid => {
        const cards = grid.querySelectorAll('.highlight-card');
        if (!cards.length) return;

        let activeIndex = 0;
        setInterval(() => {
            cards.forEach(c => c.classList.remove('icon-active-pulse'));
            if (cards[activeIndex]) {
                cards[activeIndex].classList.add('icon-active-pulse');
            }
            activeIndex = (activeIndex + 1) % cards.length;
        }, 2500);
    });
}

/* --- Left-to-Right Wipe Curtain on Tab Click --- */
let isWipeActive = false;
let isClickNavigating = false;

function triggerTabWipeTransition(targetHash) {
    const curtain = document.getElementById('tab-transition-curtain');
    if (!curtain || isWipeActive) return;

    isWipeActive = true;
    isClickNavigating = true;
    curtain.classList.remove('wipe-active');

    void curtain.offsetWidth; // Force reflow

    curtain.classList.add('wipe-active');

    setTimeout(() => {
        const targetElement = document.querySelector(targetHash);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'auto' });
        }
    }, 400);

    setTimeout(() => {
        curtain.classList.remove('wipe-active');
        isWipeActive = false;
        setTimeout(() => { isClickNavigating = false; }, 300);
    }, 850);
}

/* --- Smooth Tab Tracking Header Pill --- */
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');
    const sliderPill = document.getElementById('nav-slider-pill');
    const mobileToggle = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('mobile-active');
        });
    }

    function updateSliderPill(activeLink) {
        if (!sliderPill || !activeLink || window.innerWidth <= 768) return;
        const linkRect = activeLink.getBoundingClientRect();
        const menuRect = activeLink.parentElement.getBoundingClientRect();

        const leftOffset = linkRect.left - menuRect.left;
        sliderPill.style.transform = `translateX(${leftOffset}px)`;
        sliderPill.style.width = `${linkRect.width}px`;
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetHash = link.getAttribute('href');
            if (targetHash.startsWith('#')) {
                e.preventDefault();

                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                updateSliderPill(link);

                triggerTabWipeTransition(targetHash);

                if (navMenu.classList.contains('mobile-active')) {
                    navMenu.classList.remove('mobile-active');
                }
            }
        });
    });

    // IntersectionObserver for scroll tracking
    const observerOptions = {
        root: null,
        rootMargin: '-30% 0px -40% 0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries) => {
        if (isClickNavigating) return;

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                const matchingLink = document.querySelector(`.nav-link[href="#${id}"]`);

                if (matchingLink) {
                    navLinks.forEach(l => l.classList.remove('active'));
                    matchingLink.classList.add('active');
                    updateSliderPill(matchingLink);
                }
            }
        });
    }, observerOptions);

    sections.forEach(sec => observer.observe(sec));

    // Initial positioning
    const initialActive = document.querySelector('.nav-link.active') || navLinks[0];
    if (initialActive) updateSliderPill(initialActive);

    window.addEventListener('resize', () => {
        const currentActive = document.querySelector('.nav-link.active');
        if (currentActive) updateSliderPill(currentActive);
    });
}

/* --- Category Glass Tab Filter --- */
function initCategoryFilters() {
    const filterBtns = document.querySelectorAll('.tab-btn');
    const therapyCards = document.querySelectorAll('.therapy-card');
    const tabPill = document.getElementById('tab-slider-pill');

    function updateTabPill(activeBtn) {
        if (!tabPill || !activeBtn || window.innerWidth <= 768) return;
        const btnRect = activeBtn.getBoundingClientRect();
        const containerRect = activeBtn.parentElement.getBoundingClientRect();

        const leftOffset = btnRect.left - containerRect.left;
        tabPill.style.transform = `translateX(${leftOffset}px)`;
        tabPill.style.width = `${btnRect.width}px`;
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filterValue = btn.getAttribute('data-filter');

            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateTabPill(btn);

            therapyCards.forEach(card => {
                const category = card.getAttribute('data-category');

                if (filterValue === 'all' || category === filterValue) {
                    card.style.display = 'flex';
                    card.classList.remove('card-switching');
                    void card.offsetWidth; // Reflow
                    card.classList.add('card-switching');
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    const initialBtn = document.querySelector('.tab-btn.active') || filterBtns[0];
    if (initialBtn) updateTabPill(initialBtn);

    window.addEventListener('resize', () => {
        const currentBtn = document.querySelector('.tab-btn.active');
        if (currentBtn) updateTabPill(currentBtn);
    });
}

/* --- Scroll Reveal Animations --- */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal-slide-right');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
            }
        });
    }, {
        root: null,
        threshold: 0.08,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
}

/* --- Particle Canvas Layer --- */
function initParticleCanvas() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = 28;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 1.5 + 0.5,
            vx: (Math.random() - 0.5) * 0.25,
            vy: (Math.random() - 0.5) * 0.25,
            alpha: Math.random() * 0.35 + 0.15
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = width;
            if (p.x > width) p.x = 0;
            if (p.y < 0) p.y = height;
            if (p.y > height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(229, 213, 162, ${p.alpha})`;
            ctx.shadowBlur = 4;
            ctx.shadowColor = 'rgba(229, 213, 162, 0.4)';
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    animate();
}

function initQuickBookingDate() {
    const modalDate = document.getElementById('modal-date');
    const today = new Date().toISOString().split('T')[0];
    if (modalDate) modalDate.value = today;
}

/* --- Booking Modal Operations --- */
function openBookingModal(serviceName = null, priceRange = null) {
    const modal = document.getElementById('booking-modal');
    const serviceSelect = document.getElementById('modal-service');

    if (serviceName) {
        for (let i = 0; i < serviceSelect.options.length; i++) {
            if (serviceSelect.options[i].text.toLowerCase().includes(serviceName.toLowerCase())) {
                serviceSelect.selectedIndex = i;
                break;
            }
        }
    }

    modal.classList.add('active');
}

function closeBookingModal() {
    document.getElementById('booking-modal').classList.remove('active');
}

/* --- WhatsApp Reservation Handler --- */
function handleBookingSubmit(event) {
    event.preventDefault();

    const service = document.getElementById('modal-service').value;
    const duration = document.getElementById('modal-duration').value;
    const date = document.getElementById('modal-date').value;
    const time = document.getElementById('modal-time').value;
    const name = document.getElementById('modal-name').value;
    const phone = document.getElementById('modal-phone').value;

    const message = `*NEW RESERVATION REQUEST — AURORA INTERNATIONAL SPA*%0A%0A` +
                    `*Guest Name:* ${encodeURIComponent(name)}%0A` +
                    `*WhatsApp Phone:* ${encodeURIComponent(phone)}%0A` +
                    `*Treatment:* ${encodeURIComponent(service)}%0A` +
                    `*Duration:* ${encodeURIComponent(duration)}%0A` +
                    `*Requested Date:* ${encodeURIComponent(date)}%0A` +
                    `*Time Slot:* ${encodeURIComponent(time)}%0A%0A` +
                    `_"Breathe. You are cared for here."_`;

    const whatsappUrl = `https://wa.me/917788872255?text=${message}`;

    window.open(whatsappUrl, '_blank');
    closeBookingModal();
    alert('Thank you! Your reservation has been formatted. Opening WhatsApp to connect with Aurora Spa Concierge.');
}

/* --- Gift Voucher Controls --- */
let currentVoucherAmount = 5000;

function setVoucherAmount(amount, btnElement) {
    currentVoucherAmount = amount;
    document.querySelectorAll('.amount-pills .pill').forEach(p => p.classList.remove('active'));
    btnElement.classList.add('active');
    updateVoucherPreview();
}

function updateVoucherPreview() {
    const toInput = document.getElementById('gift-to-input').value;
    const msgInput = document.getElementById('gift-msg-input').value;

    const previewTo = document.getElementById('preview-to');
    const previewAmount = document.getElementById('preview-amount');
    const previewMsg = document.getElementById('preview-msg');

    if (previewTo) previewTo.innerText = toInput.trim() !== '' ? toInput : 'Dearest Friend';
    if (previewAmount) previewAmount.innerText = `₹ ${currentVoucherAmount.toLocaleString('en-IN')}`;
    if (previewMsg) previewMsg.innerText = msgInput.trim() !== '' ? `"${msgInput}"` : '"A moment composed with intention — breathe and enjoy pure care."';
}

function orderGiftVoucher() {
    const recipient = document.getElementById('gift-to-input').value || 'Dearest Friend';
    const msg = document.getElementById('gift-msg-input').value || 'Wishing you calm renewal.';

    const message = `*AURORA GIFT PASS ORDER*%0A%0A` +
                    `*Recipient Name:* ${encodeURIComponent(recipient)}%0A` +
                    `*Voucher Value:* ₹${currentVoucherAmount.toLocaleString('en-IN')}%0A` +
                    `*Greeting Note:* ${encodeURIComponent(msg)}%0A%0A` +
                    `_Please generate WhatsApp digital luxury pass._`;

    window.open(`https://wa.me/917788872255?text=${message}`, '_blank');
}
