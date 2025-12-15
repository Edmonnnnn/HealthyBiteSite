const HB_CONTACT_API_BASE = (window.hbGetApiBase && window.hbGetApiBase()) || "/api/v1";

function hbContactLang() {
  const raw = window.hbGetCurrentLang?.() || localStorage.getItem("hb_lang") || "en";
  return (window.hbNormalizeLang && window.hbNormalizeLang(raw)) || "en";
}

function hbEnsureStatusElement(form, selector, extraClass = "") {
  const existing = selector ? form.querySelector(selector) : null;
  if (existing) return existing;

  let fallback = form.querySelector(".hb-contact-status");
  if (!fallback) {
    fallback = document.createElement("div");
    fallback.className = `hb-contact-status${extraClass ? ` ${extraClass}` : ""}`;
    form.appendChild(fallback);
  }
  return fallback;
}

function hbHideStatuses(...elements) {
  elements.forEach((el) => {
    if (!el) return;
    el.hidden = true;
    el.classList.remove("hb-contact-status--success", "hb-contact-status--error");
  });
}

function hbShowStatus(target, message, type) {
  if (!target) return;
  target.textContent = message;
  target.hidden = false;
  target.classList.toggle("hb-contact-status--success", type === "success");
  target.classList.toggle("hb-contact-status--error", type === "error");
}

function wireSupportForm(form) {
  const successEl = hbEnsureStatusElement(
    form,
    "#contact-support-success",
    "contact-status contact-status--success hb-contact-status--success"
  );
  const errorEl = hbEnsureStatusElement(
    form,
    "#contact-support-error",
    "contact-status contact-status--error hb-contact-status--error"
  );
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    hbHideStatuses(successEl, errorEl);

    const email = form.querySelector('input[name="support-email"]')?.value?.trim() || "";
    const topic = form.querySelector('select[name="support-category"]')?.value?.trim() || "";
    const message =
      form.querySelector('textarea[name="support-message"]')?.value?.trim() || "";
    const lang = hbContactLang();
    const name =
      form.querySelector('input[name="name"]')?.value?.trim() ||
      (email ? email.split("@")[0] : "") ||
      "Healthy Bite user";

    const payload = { name, email, topic, message, lang };

    console.log("[HB contact] support request payload", payload);
    if (submitBtn) submitBtn.disabled = true;

    try {
      const response = await fetch(`${HB_CONTACT_API_BASE}/contact/support`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      let data;
      try {
        data = await response.json();
      } catch (jsonErr) {
        console.error("[HB contact] support response parse error", jsonErr);
      }

      console.log("[HB contact] support response", data);
      if (response.ok && data?.status === "ok") {
        form.reset();
        hbShowStatus(
          successEl,
          `Message sent, request ID: ${data.requestId || "support_pending"}`,
          "success"
        );
        hbHideStatuses(errorEl);
      } else {
        hbShowStatus(
          errorEl,
          "Could not send message. Please try again.",
          "error"
        );
      }
    } catch (err) {
      hbShowStatus(errorEl, "Could not send message. Please try again.", "error");
      console.error("[HB contact] support request error", err);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
}

function wireConsultForm(form) {
  const successEl = hbEnsureStatusElement(
    form,
    "#contact-consult-success",
    "contact-status contact-status--success hb-contact-status--success"
  );
  const errorEl = hbEnsureStatusElement(
    form,
    "#contact-consult-error",
    "contact-status contact-status--error hb-contact-status--error"
  );
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    hbHideStatuses(successEl, errorEl);

    const name = form.querySelector('input[name="name"]')?.value?.trim() || "";
    const email = form.querySelector('input[name="email"]')?.value?.trim() || "";
    const preferredTime =
      form.querySelector('select[name="time-window"]')?.value?.trim() || "";
    const preferredChannel = "email";
    const notes = form.querySelector('textarea[name="notes"]')?.value?.trim() || "";
    const topic = form.querySelector('select[name="topic"]')?.value?.trim() || "";
    const lang = hbContactLang();

    const message = [topic && `Topic: ${topic}`, notes].filter(Boolean).join("\n") || "";
    const payload = {
      name,
      email,
      preferredChannel,
      preferredTime,
      message,
      lang,
    };

    console.log("[HB contact] consult request payload", payload);
    if (submitBtn) submitBtn.disabled = true;

    try {
      const response = await fetch(`${HB_CONTACT_API_BASE}/contact/consult`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      let data;
      try {
        data = await response.json();
      } catch (jsonErr) {
        console.error("[HB contact] consult response parse error", jsonErr);
      }

      console.log("[HB contact] consult response", data);
      if (response.ok && data?.status === "ok") {
        form.reset();
        hbShowStatus(
          successEl,
          `Message sent, request ID: ${data.requestId || "consult_pending"}`,
          "success"
        );
        hbHideStatuses(errorEl);
      } else {
        hbShowStatus(
          errorEl,
          "Could not send message. Please try again.",
          "error"
        );
      }
    } catch (err) {
      hbShowStatus(errorEl, "Could not send message. Please try again.", "error");
      console.error("[HB contact] consult request error", err);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HB contact] init contact page");
  const supportForm = document.querySelector("#contact-support-form");
  const consultForm = document.querySelector("#contact-consult-form");

  if (supportForm) {
    wireSupportForm(supportForm);
  }
  if (consultForm) {
    wireConsultForm(consultForm);
  }
});
