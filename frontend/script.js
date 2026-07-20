const API = "";  // empty = same origin

// ---------- Mobile Nav Toggle ----------
const navToggle = document.getElementById("nav-toggle");
const navMenu = document.getElementById("nav-menu");

if (navToggle && navMenu) {
  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("open");
    navToggle.classList.toggle("open", isOpen);
    navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    document.body.classList.toggle("nav-open", isOpen);
  });

  // Close menu when a link is tapped
  navMenu.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("open");
      navToggle.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    });
  });
}

// ---------- Smooth Scrolling ----------
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ---------- Load Skills ----------
async function loadSkills() {
  try {
    const res = await fetch(`${API}/api/skills`);
    const skills = await res.json();
    const grid = document.getElementById("skills-grid");
    grid.innerHTML = skills.map(s => `
      <div class="skill-card" tabindex="0">
        <div class="skill-name">${s.name}</div>
        <div class="skill-cat">${s.category}</div>
        <div class="skill-bar">
          <div class="skill-fill" data-level="${s.level}"></div>
        </div>
      </div>
    `).join("");

    // Animate bars on scroll
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.querySelectorAll(".skill-fill").forEach(bar => {
            bar.style.width = bar.dataset.level + "%";
          });
        }
      });
    }, { threshold: 0.2 });
    observer.observe(grid);
  } catch (err) {
    document.getElementById("skills-grid").innerHTML = `<p class="loading">Could not load skills.</p>`;
  }
}

// ---------- Load Projects ----------
async function loadProjects() {
  try {
    const res = await fetch(`${API}/api/projects`);
    const projects = await res.json();
    const grid = document.getElementById("projects-grid");
    if (!projects.length) {
      grid.innerHTML = `<p class="loading">No projects yet.</p>`;
      return;
    }
    grid.innerHTML = projects.map(p => `
      <div class="project-card">
        ${p.image ? `<img src="${p.image}" alt="${p.title}" class="project-image">` : ""}
        <div class="project-card-content">
          <h3>${p.title}</h3>
          <p>${p.description}</p>
          <div class="tech-tags">
            ${p.tech_stack.map(t => `<span class="tech-tag">${t}</span>`).join("")}
          </div>
          <div class="project-links">
            ${p.github_url ? `<a href="${p.github_url}" target="_blank">GitHub →</a>` : ""}
            ${p.live_url   ? `<a href="${p.live_url}"   target="_blank">Live demo →</a>` : ""}
          </div>
        </div>
      </div>
    `).join("");
  } catch (err) {
    document.getElementById("projects-grid").innerHTML = `<p class="loading">Could not load projects.</p>`;
  }
}

// ---------- Contact Form ----------
document.getElementById("contact-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("submit-btn");
  const msg = document.getElementById("form-msg");
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const message = document.getElementById("message").value.trim();
  
  // Validation
  if (!name || !email || !message) {
    msg.textContent = "Please fill in all fields.";
    msg.classList.remove("success");
    msg.classList.add("error");
    return;
  }
  
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    msg.textContent = "Please enter a valid email address.";
    msg.classList.remove("success");
    msg.classList.add("error");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Sending...";
  msg.textContent = "";
  msg.className = "form-feedback";

  const body = {
    name: name,
    email: email,
    message: message,
  };

  try {
    const res = await fetch(`${API}/api/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (res.ok) {
      msg.textContent = "✓ Message sent successfully! I'll get back to you soon.";
      msg.classList.add("success");
      e.target.reset();
    } else {
      msg.textContent = data.detail || "Something went wrong.";
      msg.classList.add("error");
    }
  } catch {
    msg.textContent = "Network error. Please try again.";
    msg.classList.add("error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Send message →";
  }
});

// ---------- Init ----------
loadSkills();
loadProjects();

// ---------- Scroll Reveal ----------
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll(".reveal").forEach(el => revealObserver.observe(el));