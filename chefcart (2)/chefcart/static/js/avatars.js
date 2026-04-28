/**
 * ChefCart – Indian Chef Avatar Generator
 * Draws unique, colourful illustrated avatars on <canvas> elements.
 * Each avatar is based on the chef's name initial + a warm colour palette.
 */

const CHEF_AVATARS = {
  // id → { skin, turban/dupatta colour, accent, style }
  1:  { bg:"#F4A460", skin:"#8B5E3C", hair:"#2C1810", accent:"#E07020", hat:"toque" },
  2:  { bg:"#E8A0BF", skin:"#C68642", hair:"#1A0A00", accent:"#D4609A", hat:"bun"   },
  3:  { bg:"#87CEEB", skin:"#8B6914", hair:"#0D0D0D", accent:"#2060C0", hat:"toque" },
  4:  { bg:"#DDA0DD", skin:"#C09060", hair:"#1A0800", accent:"#9040A0", hat:"bun"   },
  5:  { bg:"#F0A050", skin:"#7A4828", hair:"#100800", accent:"#C05010", hat:"toque" },
  6:  { bg:"#98D8C8", skin:"#B07840", hair:"#0D0500", accent:"#20907A", hat:"bun"   },
  7:  { bg:"#FFB347", skin:"#9B6B3A", hair:"#080400", accent:"#D06000", hat:"toque" },
  8:  { bg:"#F4C2C2", skin:"#B87850", hair:"#100400", accent:"#C05060", hat:"bun"   },
  9:  { bg:"#B0C4DE", skin:"#7A4828", hair:"#0D0800", accent:"#304070", hat:"toque" },
  10: { bg:"#FFDAB9", skin:"#C07040", hair:"#080400", accent:"#C06030", hat:"bun"   },
};

function drawChefAvatar(canvas, chefId, name) {
  const cfg = CHEF_AVATARS[chefId] || {
    bg:"#E8C88A", skin:"#A0703A", hair:"#1A0800", accent:"#8B4513", hat:"toque"
  };
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  const cx = W / 2;

  // Background
  ctx.fillStyle = cfg.bg;
  ctx.fillRect(0, 0, W, H);

  // Subtle radial gradient overlay
  const grad = ctx.createRadialGradient(cx, H * 0.3, 10, cx, H * 0.3, W * 0.7);
  grad.addColorStop(0, "rgba(255,255,255,0.25)");
  grad.addColorStop(1, "rgba(0,0,0,0.12)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  // ── Body / Shoulders ────────────────────────────────────────────
  ctx.fillStyle = cfg.accent;
  ctx.beginPath();
  ctx.ellipse(cx, H * 1.05, W * 0.42, H * 0.38, 0, 0, Math.PI * 2);
  ctx.fill();

  // Collar / chef uniform detail
  ctx.fillStyle = "#FFFFFF";
  ctx.beginPath();
  ctx.ellipse(cx, H * 0.88, W * 0.15, H * 0.14, 0, 0, Math.PI * 2);
  ctx.fill();

  // ── Neck ────────────────────────────────────────────────────────
  ctx.fillStyle = cfg.skin;
  ctx.beginPath();
  ctx.roundRect(cx - W * 0.07, H * 0.55, W * 0.14, H * 0.18, 4);
  ctx.fill();

  // ── Head ────────────────────────────────────────────────────────
  ctx.fillStyle = cfg.skin;
  ctx.beginPath();
  ctx.ellipse(cx, H * 0.44, W * 0.24, H * 0.26, 0, 0, Math.PI * 2);
  ctx.fill();

  // ── Hair ────────────────────────────────────────────────────────
  ctx.fillStyle = cfg.hair;
  ctx.beginPath();
  ctx.ellipse(cx, H * 0.30, W * 0.24, H * 0.145, 0, Math.PI, 0);
  ctx.fill();

  // Side hair
  ctx.beginPath();
  ctx.ellipse(cx - W * 0.22, H * 0.42, W * 0.06, H * 0.12, -0.3, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(cx + W * 0.22, H * 0.42, W * 0.06, H * 0.12, 0.3, 0, Math.PI * 2);
  ctx.fill();

  if (cfg.hat === "bun") {
    // Bun / tied hair for female chefs
    ctx.fillStyle = cfg.hair;
    ctx.beginPath();
    ctx.ellipse(cx, H * 0.17, W * 0.1, H * 0.09, 0, 0, Math.PI * 2);
    ctx.fill();
    // Hair tie
    ctx.strokeStyle = cfg.accent;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(cx, H * 0.17, W * 0.06, 0, Math.PI * 2);
    ctx.stroke();
  } else {
    // Chef toque (tall white hat)
    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.roundRect(cx - W * 0.17, H * 0.04, W * 0.34, H * 0.23, [W * 0.06, W * 0.06, 0, 0]);
    ctx.fill();
    // Hat band
    ctx.fillStyle = cfg.accent;
    ctx.fillRect(cx - W * 0.185, H * 0.24, W * 0.37, H * 0.04);
    // Hat puff lines
    ctx.strokeStyle = "rgba(200,200,200,0.6)";
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 3; i++) {
      ctx.beginPath();
      ctx.moveTo(cx - W * 0.1 + i * W * 0.1, H * 0.07);
      ctx.lineTo(cx - W * 0.1 + i * W * 0.1, H * 0.24);
      ctx.stroke();
    }
  }

  // ── Eyes ────────────────────────────────────────────────────────
  const eyeY = H * 0.44;
  [-1, 1].forEach(function(side) {
    const ex = cx + side * W * 0.09;
    // White
    ctx.fillStyle = "#FFF";
    ctx.beginPath();
    ctx.ellipse(ex, eyeY, W * 0.045, H * 0.030, 0, 0, Math.PI * 2);
    ctx.fill();
    // Iris
    ctx.fillStyle = "#3B2007";
    ctx.beginPath();
    ctx.ellipse(ex, eyeY, W * 0.025, H * 0.022, 0, 0, Math.PI * 2);
    ctx.fill();
    // Highlight
    ctx.fillStyle = "#FFF";
    ctx.beginPath();
    ctx.ellipse(ex + W * 0.01, eyeY - H * 0.007, W * 0.008, H * 0.008, 0, 0, Math.PI * 2);
    ctx.fill();
    // Eyelash line
    ctx.strokeStyle = cfg.hair;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.ellipse(ex, eyeY, W * 0.047, H * 0.032, 0, Math.PI, 0);
    ctx.stroke();
  });

  // ── Eyebrows ────────────────────────────────────────────────────
  ctx.strokeStyle = cfg.hair;
  ctx.lineWidth = 2.5;
  ctx.lineCap = "round";
  [-1, 1].forEach(function(side) {
    const ex = cx + side * W * 0.09;
    ctx.beginPath();
    ctx.moveTo(ex - W * 0.05, eyeY - H * 0.058);
    ctx.quadraticCurveTo(ex, eyeY - H * 0.068, ex + W * 0.05, eyeY - H * 0.058);
    ctx.stroke();
  });

  // ── Nose ────────────────────────────────────────────────────────
  ctx.strokeStyle = shadeColor(cfg.skin, -30);
  ctx.lineWidth = 1.8;
  ctx.beginPath();
  ctx.moveTo(cx, H * 0.47);
  ctx.quadraticCurveTo(cx + W * 0.04, H * 0.53, cx, H * 0.54);
  ctx.stroke();

  // ── Smile ───────────────────────────────────────────────────────
  ctx.strokeStyle = shadeColor(cfg.skin, -50);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, H * 0.54, W * 0.07, 0.15, Math.PI - 0.15);
  ctx.stroke();

  // Teeth
  ctx.fillStyle = "#FFF";
  ctx.beginPath();
  ctx.ellipse(cx, H * 0.562, W * 0.055, H * 0.022, 0, 0, Math.PI * 2);
  ctx.fill();

  // ── Name Label at bottom ────────────────────────────────────────
  ctx.fillStyle = "rgba(0,0,0,0.45)";
  ctx.fillRect(0, H * 0.84, W, H * 0.16);

  ctx.fillStyle = "#FFFFFF";
  ctx.font = "bold " + Math.round(W * 0.095) + "px 'Playfair Display', serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  // Shorten long names
  const parts = name.split(" ");
  const label = parts.length > 1 ? parts[0] + " " + parts[1][0] + "." : name;
  ctx.fillText(label, cx, H * 0.915);
}

function shadeColor(hex, amt) {
  const num = parseInt(hex.replace("#",""), 16);
  const r = Math.min(255, Math.max(0, (num >> 16) + amt));
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0xff) + amt));
  const b = Math.min(255, Math.max(0, (num & 0xff) + amt));
  return "#" + ((r << 16) | (g << 8) | b).toString(16).padStart(6, "0");
}

// ── Auto-render all chef avatar placeholders on page load ───────────────────
document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("canvas[data-chef-id]").forEach(function(canvas) {
    const id   = parseInt(canvas.getAttribute("data-chef-id"));
    const name = canvas.getAttribute("data-chef-name") || "";
    drawChefAvatar(canvas, id, name);
  });
});
