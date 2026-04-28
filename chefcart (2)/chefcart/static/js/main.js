/**
 * ChefCart – Main JavaScript
 * Handles: flash auto-dismiss, form validation, star picker UX
 */

// ── Auto-dismiss flash messages after 4 seconds ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(flash => {
    setTimeout(() => {
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(20px)';
      flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      setTimeout(() => flash.remove(), 400);
    }, 4000);
  });

  // ── Set today's date as minimum for booking form ───────────────────────────
  const dateInput = document.getElementById('date');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
  }

  // ── Basic client-side form validation ─────────────────────────────────────
  document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', e => {
      const inputs = form.querySelectorAll('input[required]');
      let valid = true;
      inputs.forEach(input => {
        if (!input.value.trim()) {
          input.style.borderColor = '#D04040';
          valid = false;
        } else {
          input.style.borderColor = '';
        }
      });
      if (!valid) {
        e.preventDefault();
        alert('Please fill in all required fields.');
      }
    });
  });

  // ── Booking form validation ────────────────────────────────────────────────
  const bookingForm = document.querySelector('.booking-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', e => {
      const date  = bookingForm.querySelector('[name="date"]').value;
      const slot  = bookingForm.querySelector('[name="time_slot"]').value;
      if (!date || !slot) {
        e.preventDefault();
        alert('Please select both a date and a time slot.');
      }
    });
  }

  // ── Review form: require star rating ──────────────────────────────────────
  const reviewForm = document.querySelector('.review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', e => {
      const rating = reviewForm.querySelector('#ratingInput').value;
      if (!rating) {
        e.preventDefault();
        alert('Please select a star rating before submitting.');
      }
    });
  }

  // ── Smooth price update in booking summary ─────────────────────────────────
  // (Already handled by Jinja template; this is a placeholder for future use)
});
