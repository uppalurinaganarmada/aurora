/* ==========================================================================
   AURORA INTERNATIONAL SPA — INTERACTIVE LOGIC & ANIMATIONS (VOL ONE 2026)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initIntroCurtain();
    initNavigation();
    initCategoryFilters();
    initQuickBookingDate();
    initScrollReveal();
    initParticleCanvas();
    initSequentialIconHighlight();
    updateVoucherPreview();
});

/* --- Luxury Intro Curtain Reveal Animation (Silky Breathing Aura) --- */
function initIntroCurtain() {
    const introCurtain = document.getElementById('intro-curtain');
    if (!introCurtain) return;

    // Show logo intro with silky breathing silver halo, then raise curtain after 2.4 seconds
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

/* --- Increased 2.5-Second Sequential Highlight Loop for Amenity & Etiquette Icons --- */
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

    // Jump to exact section position at the mid-point of the silver curtain wipe
    setTimeout(() => {
        if (targetHash && targetHash.startsWith('#')) {
            const targetSec = document.querySelector(targetHash);
            if (targetSec) {
                const navbarHeight = 70;
                const targetPosition = targetSec.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'instant'
                });
                
                // Re-trigger slide-in animation for elements in target section
                const slideEls = targetSec.querySelectorAll('.reveal-slide-right');
                slideEls.forEach(el => {
                    el.classList.remove('reveal-active');
                    void el.offsetWidth;
                    el.classList.add('reveal-active');
                });
            }
        }
    }, 380);

    setTimeout(() => {
        curtain.classList.remove('wipe-active');
        isWipeActive = false;
        isClickNavigating = false;
    }, 850);
}

function initNavigation() {
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const navPill = document.getElementById('nav-slider-pill');

    function updateNavPill(activeLink) {
        if (!navPill || !navMenu || !activeLink) return;
        const linkRect = activeLink.getBoundingClientRect();
        const menuRect = navMenu.getBoundingClientRect();

        const offsetLeft = linkRect.left - menuRect.left;
        const width = linkRect.width;

        navPill.style.transform = `translateX(${offsetLeft}px)`;
        navPill.style.width = `${width}px`;
    }

    const activeLink = document.querySelector('.nav-link.active');
    if (activeLink) {
        setTimeout(() => updateNavPill(activeLink), 100);
    }

    window.addEventListener('resize', () => {
        const currentActive = document.querySelector('.nav-link.active');
        if (currentActive) updateNavPill(currentActive);
    });

    const sections = document.querySelectorAll('section[id]');

    // Scroll Detection (Updates navbar link active state & pill ONLY when scrolling)
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        if (isClickNavigating) return;

        let detectedSectionId = '';
        sections.forEach(sec => {
            const secTop = sec.offsetTop - 140;
            const secHeight = sec.offsetHeight;
            if (window.scrollY >= secTop && window.scrollY < secTop + secHeight) {
                detectedSectionId = sec.getAttribute('id');
            }
        });

        if (detectedSectionId) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${detectedSectionId}`) {
                    link.classList.add('active');
                    updateNavPill(link);
                }
            });
        }
    });

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('mobile-active');
        });
    }

    // Header Nav Link Click Handler
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            
            if (navMenu) navMenu.classList.remove('mobile-active');
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            updateNavPill(link);

            triggerTabWipeTransition(href);
        });
    });
}

/* --- Menu Category Filter Switcher --- */
function initCategoryFilters() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const cards = document.querySelectorAll('.therapy-card');
    const pill = document.getElementById('tab-slider-pill');
    const container = document.getElementById('category-tabs-container');

    function updatePillPosition(activeBtn) {
        if (!pill || !container || !activeBtn) return;
        const btnRect = activeBtn.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        const offsetLeft = btnRect.left - containerRect.left;
        const width = btnRect.width;

        pill.style.transform = `translateX(${offsetLeft}px)`;
        pill.style.width = `${width}px`;
    }

    const activeBtn = document.querySelector('.tab-btn.active');
    if (activeBtn) {
        setTimeout(() => updatePillPosition(activeBtn), 100);
    }

    window.addEventListener('resize', () => {
        const currentActive = document.querySelector('.tab-btn.active');
        if (currentActive) updatePillPosition(currentActive);
    });

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.classList.contains('active')) return;

            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            updatePillPosition(btn);

            const filter = btn.getAttribute('data-filter');
            let visibleCount = 0;

            cards.forEach(card => {
                const matches = filter === 'all' || card.getAttribute('data-category') === filter;

                if (matches) {
                    card.style.display = 'flex';
                    card.classList.remove('card-switching');
                    void card.offsetWidth;
                    card.style.animationDelay = `${visibleCount * 0.06}s`;
                    card.classList.add('card-switching');
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                    card.classList.remove('card-switching');
                }
            });
        });
    });
}

/* --- 100% RELIABLE WEB AUDIO API SPA SOUNDSCAPE ENGINE --- */
let audioCtx = null;
let isPlayingAudio = false;
let activeOscillators = [];
let masterGain = null;

function toggleAudio() {
    const btn = document.getElementById('sound-toggle-btn');
    const icon = document.getElementById('sound-icon');
    const htmlAudio = document.getElementById('spa-audio');

    if (!isPlayingAudio) {
        try {
            startWebAudioSpaSoundscape();
            isPlayingAudio = true;
            if (btn) btn.classList.add('playing');
            if (icon) icon.className = 'fa-solid fa-volume-high';
        } catch (e) {
            console.log('Web Audio fallback to HTML Audio:', e);
            if (htmlAudio) {
                htmlAudio.play().then(() => {
                    isPlayingAudio = true;
                    if (btn) btn.classList.add('playing');
                    if (icon) icon.className = 'fa-solid fa-volume-high';
                });
            }
        }
    } else {
        stopWebAudioSpaSoundscape();
        if (htmlAudio) htmlAudio.pause();
        isPlayingAudio = false;
        if (btn) btn.classList.remove('playing');
        if (icon) icon.className = 'fa-solid fa-volume-xmark';
    }
}

function startWebAudioSpaSoundscape() {
    if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContext();
    }
    
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    stopWebAudioSpaSoundscape();

    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.01, audioCtx.currentTime);
    masterGain.gain.exponentialRampToValueAtTime(0.28, audioCtx.currentTime + 3);
    masterGain.connect(audioCtx.destination);

    // Harmonic 432Hz Zen Chords (432Hz A, 216Hz A, 324Hz E, 540Hz C#)
    const freqs = [108, 216, 324, 432, 540];

    freqs.forEach(freq => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

        const lfo = audioCtx.createOscillator();
        const lfoGain = audioCtx.createGain();
        lfo.frequency.setValueAtTime(0.12, audioCtx.currentTime);
        lfoGain.gain.setValueAtTime(1.5, audioCtx.currentTime);
        lfo.connect(osc.frequency);
        lfo.start();

        gain.gain.setValueAtTime(0.15 / freqs.length, audioCtx.currentTime);

        osc.connect(gain);
        gain.connect(masterGain);
        osc.start();

        activeOscillators.push(osc, lfo);
    });
}

function stopWebAudioSpaSoundscape() {
    if (masterGain && audioCtx) {
        try {
            masterGain.gain.setValueAtTime(masterGain.gain.value, audioCtx.currentTime);
            masterGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.8);
        } catch(e) {}
    }

    setTimeout(() => {
        activeOscillators.forEach(osc => {
            try { osc.stop(); osc.disconnect(); } catch (e) {}
        });
        activeOscillators = [];
    }, 850);
}

/* --- Scroll Reveal Animations --- */
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                obs.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-slide-right').forEach(el => {
        observer.observe(el);
    });
}

/* --- Floating Particle Canvas (Sterling Silver & Emerald Teal Sparkles) --- */
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
    const particleCount = 42;
    const colors = ['rgba(224, 230, 237, 0.45)', 'rgba(60, 170, 160, 0.4)', 'rgba(255, 255, 255, 0.35)'];

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 2.2 + 0.8,
            color: colors[Math.floor(Math.random() * colors.length)],
            speedY: Math.random() * 0.4 + 0.1,
            speedX: (Math.random() - 0.5) * 0.2
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 8;
            ctx.shadowColor = p.color;
            ctx.fill();

            p.y -= p.speedY;
            p.x += p.speedX;

            if (p.y < -10) {
                p.y = height + 10;
                p.x = Math.random() * width;
            }
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

    window.open(`https://wa.me/917788872255?text=`, '_blank');
}
