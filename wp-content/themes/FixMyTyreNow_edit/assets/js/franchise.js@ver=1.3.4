/* Franchise Registration — Postcode tag input, fee preview, Revolut payment */
(function () {
    'use strict';

    if (!document.getElementById('franchise-reg-form')) return;

    const cfg     = window.fmtnFranchiseConfig || {};
    const tiers   = (cfg.tiers || []).map(t => ({ prefix: t.prefix, monthly_rate: parseFloat(t.monthly_rate) || 0 }));
    const defRate = parseFloat(cfg.defaultRate) || 25;
    const restUrl = cfg.restUrl;
    const nonce   = cfg.nonce;

    const postcodes = [];

    // ── Postcode tag input ────────────────────────────────────────────────────

    const tagContainer = document.getElementById('freg-postcode-tags');
    const tagInput     = document.getElementById('freg-postcode-input');

    function getPrefix(district) {
        const m = district.match(/^([A-Z]{1,2})/i);
        return m ? m[1].toUpperCase() : '';
    }

    function getRateForDistrict(district) {
        const d = district.toUpperCase().replace(/\s+/g, '');
        // Match tiers: longest matching prefix wins (e.g. "SW1" beats "SW" for SW1A)
        // Supports exact district match (e.g. tier "NW10") OR area prefix match (e.g. tier "NW")
        let matched = null;
        let matchLen = 0;
        tiers.forEach(function(t) {
            const p = t.prefix.toUpperCase();
            if (d === p || d.startsWith(p)) {
                if (p.length > matchLen) {
                    matched = t;
                    matchLen = p.length;
                }
            }
        });
        return matched ? parseFloat(matched.monthly_rate) : defRate;
    }

    function updateFeePreview() {
        const preview   = document.getElementById('freg-fee-preview');
        const totalEl   = document.getElementById('freg-fee-total');
        const rowsEl    = document.getElementById('freg-fee-rows');

        if (postcodes.length === 0) {
            preview.style.display = 'none';
            return;
        }

        let sum = 0;
        rowsEl.innerHTML = '';
        postcodes.forEach(pc => {
            const rate = getRateForDistrict(pc);
            sum += rate;
            const tr = document.createElement('tr');
            tr.innerHTML = '<td>' + pc + '</td><td>£' + rate.toFixed(2) + ' / ay</td>';
            rowsEl.appendChild(tr);
        });

        totalEl.textContent = '£' + sum.toFixed(2);
        preview.style.display = 'block';
    }

    function addPostcode(raw) {
        const normalised = raw.toUpperCase().replace(/\s+/g, '');
        if (!/^[A-Z]{1,2}[0-9][0-9A-Z]?$/.test(normalised)) {
            showError('Invalid postcode: ' + raw + '. Use district format e.g. NW10, W5');
            return;
        }
        if (postcodes.includes(normalised)) return;
        postcodes.push(normalised);

        const rate = getRateForDistrict(normalised);

        const tag = document.createElement('span');
        tag.className = 'freg-tag';

        const labelNode = document.createTextNode(normalised + ' ');
        const rateNode  = document.createElement('em');
        rateNode.className = 'freg-tag-rate';
        rateNode.textContent = '£' + rate.toFixed(2) + '/ay';

        const remove = document.createElement('button');
        remove.type = 'button';
        remove.textContent = '×';
        remove.setAttribute('aria-label', 'Remove ' + normalised);
        remove.onclick = () => {
            postcodes.splice(postcodes.indexOf(normalised), 1);
            tag.remove();
            updateFeePreview();
        };

        tag.appendChild(labelNode);
        tag.appendChild(rateNode);
        tag.appendChild(remove);
        tagContainer.insertBefore(tag, tagInput);
        tagInput.value = '';
        updateFeePreview();
    }

    tagInput.addEventListener('keydown', e => {
        if (['Enter', ',', ' '].includes(e.key)) {
            e.preventDefault();
            const v = tagInput.value.trim();
            if (v) addPostcode(v);
        }
        if (e.key === 'Backspace' && tagInput.value === '' && postcodes.length) {
            const last = tagContainer.querySelectorAll('.freg-tag');
            if (last.length) last[last.length - 1].querySelector('button').click();
        }
    });

    tagContainer.addEventListener('click', () => tagInput.focus());

    // ── Form submission ───────────────────────────────────────────────────────

    function showError(msg) {
        const el = document.getElementById('freg-error');
        el.textContent = msg;
        el.style.display = 'block';
    }

    function hideError() {
        const el = document.getElementById('freg-error');
        el.style.display = 'none';
    }

    document.getElementById('franchise-reg-form').addEventListener('submit', async e => {
        e.preventDefault();
        hideError();

        if (postcodes.length === 0) {
            showError('Please add at least one postcode.');
            return;
        }

        const btn = document.getElementById('freg-submit');
        btn.disabled = true;
        btn.textContent = 'Processing…';

        const body = {
            nonce,
            business_name:   document.getElementById('freg-business-name').value,
            contact_name:    document.getElementById('freg-contact-name').value,
            email:           document.getElementById('freg-email').value,
            phone:           document.getElementById('freg-phone').value,
            vehicle_details: document.getElementById('freg-vehicle').value,
            service_types:   [...document.querySelectorAll('[name="service_types[]"]:checked')].map(c => c.value),
            postcodes,
        };

        try {
            const res  = await fetch(restUrl + 'franchise/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-FMTN-Nonce': nonce },
                body: JSON.stringify(body),
            });
            const data = await res.json();

            if (!res.ok || data.error) {
                showError(data.error || 'Something went wrong. Please try again.');
                btn.disabled = false;
                btn.textContent = 'Continue to Payment';
                return;
            }

            // Show Revolut widget
            document.getElementById('franchise-reg-form').style.display = 'none';
            document.getElementById('freg-payment-section').style.display = 'block';
            document.getElementById('freg-payment-fee').textContent = '£' + parseFloat(data.fee).toFixed(2) + '/month';

            const revolut = RevolutCheckout(data.revolut_public_id);
            revolut.payWithPopup({
                onSuccess: async () => {
                    // Confirm payment server-side
                    const confirmRes = await fetch(restUrl + 'franchise/payment-confirm', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nonce, revolut_order_id: data.revolut_order_id }),
                    });
                    const confirmData = await confirmRes.json();
                    if (confirmData.success) {
                        document.getElementById('freg-payment-section').style.display = 'none';
                        document.getElementById('freg-success').style.display = 'block';
                    } else {
                        showError('Payment confirmed but we could not record it. Please contact us with your reference.');
                        document.getElementById('freg-payment-section').style.display = 'none';
                        document.getElementById('franchise-reg-form').style.display = 'block';
                    }
                },
                onError: (message) => {
                    showError('Payment failed: ' + message);
                    document.getElementById('freg-payment-section').style.display = 'none';
                    document.getElementById('franchise-reg-form').style.display = 'block';
                    btn.disabled = false;
                    btn.textContent = 'Continue to Payment';
                },
                onCancel: () => {
                    document.getElementById('freg-payment-section').style.display = 'none';
                    document.getElementById('franchise-reg-form').style.display = 'block';
                    btn.disabled = false;
                    btn.textContent = 'Continue to Payment';
                },
            });

        } catch (err) {
            showError('Network error. Please try again.');
            btn.disabled = false;
            btn.textContent = 'Continue to Payment';
        }
    });

}());
