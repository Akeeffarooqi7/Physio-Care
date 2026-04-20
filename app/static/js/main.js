// ===== PhysioCare Main JS =====

document.addEventListener('DOMContentLoaded', () => {

  // ---- Navbar scroll effect ----
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ---- Auto-dismiss flash messages ----
  document.querySelectorAll('.flash-alert').forEach(el => {
    setTimeout(() => {
      el.style.animation = 'slideOutRight 0.4s ease forwards';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });

  // ---- Animated counter for stats ----
  const counters = document.querySelectorAll('[data-count]');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.count);
      const suffix = el.dataset.suffix || '';
      const duration = 2000;
      const step = target / (duration / 16);
      let current = 0;
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = Math.floor(current).toLocaleString() + suffix;
        if (current >= target) clearInterval(timer);
      }, 16);
      counterObserver.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(el => counterObserver.observe(el));

  // ---- Interactive Body Map ----
  const hotspots = document.querySelectorAll('.body-hotspot');
  hotspots.forEach(spot => {
    spot.addEventListener('click', async () => {
      const part = spot.dataset.part;

      // Highlight active
      hotspots.forEach(s => s.classList.remove('active'));
      spot.classList.add('active');

      // Show loading
      const panel = document.getElementById('bodyInfoPanel');
      if (!panel) return;

      panel.innerHTML = `
        <div class="text-center py-5">
          <div class="spinner-border text-primary" style="width:3rem;height:3rem;"></div>
          <p class="mt-3 text-muted">Loading information...</p>
        </div>`;

      try {
        const res = await fetch(`/api/body-info/${part}`);
        const data = await res.json();
        renderBodyInfo(panel, data);
      } catch (e) {
        panel.innerHTML = `<div class="alert alert-danger">Failed to load. Please try again.</div>`;
      }
    });
  });

  function renderBodyInfo(panel, data) {
    const symptomsHTML = data.symptoms.map(s =>
      `<li><i class="fas fa-circle-dot me-2" style="color:${data.color};font-size:10px"></i>${s}</li>`
    ).join('');
    const exercisesHTML = data.exercises.map(e =>
      `<li><i class="fas fa-dumbbell me-2 text-primary" style="font-size:12px"></i>${e}</li>`
    ).join('');
    const dietHTML = data.diet.map(d =>
      `<li><i class="fas fa-leaf me-2 text-success" style="font-size:12px"></i>${d}</li>`
    ).join('');

    panel.innerHTML = `
      <div class="body-info-content active">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div style="width:52px;height:52px;background:${data.color}20;border-radius:12px;
               display:flex;align-items:center;justify-content:center;font-size:26px;flex-shrink:0;">
            ${data.icon}
          </div>
          <div>
            <h3 class="mb-1" style="color:${data.color}">${data.title}</h3>
            <p class="mb-0 text-muted" style="font-size:13px">${data.description}</p>
          </div>
        </div>
        <div class="row g-3">
          <div class="col-12">
            <div class="info-section">
              <h6><i class="fas fa-stethoscope me-2"></i>Common Symptoms</h6>
              <ul class="info-list">${symptomsHTML}</ul>
            </div>
          </div>
          <div class="col-12">
            <div class="info-section">
              <h6><i class="fas fa-dumbbell me-2"></i>Recommended Exercises</h6>
              <ul class="info-list">${exercisesHTML}</ul>
            </div>
          </div>
          <div class="col-12">
            <div class="info-section">
              <h6><i class="fas fa-apple-alt me-2"></i>Diet Recommendations</h6>
              <ul class="info-list">${dietHTML}</ul>
            </div>
          </div>
          <div class="col-12">
            <a href="/appointments/book" class="btn btn-primary w-100">
              <i class="fas fa-calendar-plus me-2"></i>Book Treatment Appointment
            </a>
          </div>
        </div>
      </div>`;
  }

  // ---- Appointment time slot selector ----
  const timeSlotBtns = document.querySelectorAll('.time-slot-btn');
  const timeInput = document.getElementById('preferredTimeInput');
  timeSlotBtns.forEach(btn => {
    if (!btn.classList.contains('booked')) {
      btn.addEventListener('click', () => {
        timeSlotBtns.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        if (timeInput) timeInput.value = btn.dataset.time;
      });
    }
  });

  // ---- Date change: load available slots ----
  const dateInput = document.getElementById('preferredDate');
  if (dateInput) {
    dateInput.addEventListener('change', async () => {
      const date = dateInput.value;
      if (!date) return;
      try {
        const res = await fetch(`/appointments/check-slots?date=${date}`);
        const data = await res.json();
        timeSlotBtns.forEach(btn => {
          const time = btn.dataset.time;
          btn.classList.remove('selected', 'booked');
          if (data.booked.includes(time)) {
            btn.classList.add('booked');
            btn.title = 'Already booked';
          }
        });
        if (timeInput) timeInput.value = '';
      } catch(e) {}
    });
  }

  // ---- Contact form via AJAX ----
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = contactForm.querySelector('[type="submit"]');
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Sending...';

      const formData = new FormData(contactForm);
      const data = Object.fromEntries(formData);

      try {
        const res = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        const result = await res.json();
        if (result.success) {
          showToast('Message sent successfully! We\'ll get back to you soon.', 'success');
          contactForm.reset();
        } else {
          showToast('Failed to send message. Please try again.', 'danger');
        }
      } catch(e) {
        showToast('Network error. Please try again.', 'danger');
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Send Message';
      }
    });
  }

  // ---- Exercise accordion ----
  document.querySelectorAll('.exercise-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = document.getElementById(btn.dataset.target);
      if (!target) return;
      const isOpen = !target.classList.contains('d-none');
      target.classList.toggle('d-none', isOpen);
      btn.querySelector('i').classList.toggle('fa-chevron-down', isOpen);
      btn.querySelector('i').classList.toggle('fa-chevron-up', !isOpen);
    });
  });

  // ---- Treatment filter tabs ----
  document.querySelectorAll('[data-filter]').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('[data-filter]').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.dataset.filter;
      document.querySelectorAll('[data-category]').forEach(card => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.closest('.col').style.display = show ? '' : 'none';
      });
    });
  });

  // ---- Smooth scroll for anchor links ----
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ---- Back to top ----
  const btt = document.getElementById('backToTop');
  if (btt) {
    window.addEventListener('scroll', () => {
      btt.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }
});

// ---- Toast helper ----
function showToast(message, type = 'success') {
  const container = document.getElementById('flashContainer') ||
    (() => {
      const c = document.createElement('div');
      c.id = 'flashContainer';
      c.className = 'flash-container';
      document.body.appendChild(c);
      return c;
    })();

  const toast = document.createElement('div');
  toast.className = `flash-alert flash-${type}`;
  const icons = { success: 'check-circle', danger: 'exclamation-circle', warning: 'exclamation-triangle', info: 'info-circle' };
  toast.innerHTML = `<i class="fas fa-${icons[type] || 'info-circle'} me-2"></i>${message}
    <button class="flash-close" onclick="this.parentElement.remove()">×</button>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 6000);
}
