/* FixMyTyreNow — Booking Form (Revolut Merchant in-page payment) */
( function () {
    'use strict';

    const form = document.getElementById( 'fmtn-booking-form' );
    if ( ! form ) return;

    const config     = window.fmtnConfig || {};
    const submitWrap = form.querySelector( '#fmtn-submit-wrap' );
    const submitBtn  = form.querySelector( '#fmtn-submit-btn' );
    if ( ! submitBtn ) return;

    const btnText = submitBtn.querySelector( '.btn-text' );
    const btnLoad = submitBtn.querySelector( '.btn-loading' );
    const msgBox  = form.querySelector( '#fmtn-booking-msg' );

    // Revolut payment section elements
    const revolutSection = document.getElementById( 'revolut-payment-section' );
    const revolutPayBtn  = document.getElementById( 'revolut-pay-btn' );
    const revolutPayMsg  = document.getElementById( 'revolut-pay-msg' );

    // ── Mode toggle ───────────────────────────────────────────────────────────
    let currentMode = 'emergency';

    const modeToggle      = document.getElementById( 'booking-mode-toggle' );
    const blockEmergency  = document.getElementById( 'bf-emergency' );
    const blockScheduled  = document.getElementById( 'bf-scheduled' );
    const bookingTypeInput = form.querySelector( '#booking_type' );

    function switchMode( mode ) {
        if ( ! modeToggle || ! blockEmergency || ! blockScheduled || ! bookingTypeInput ) return;

        currentMode = mode;
        bookingTypeInput.value = mode;

        var isEmergency = mode === 'emergency';

        blockEmergency.classList.toggle( 'bf-hidden', ! isEmergency );
        blockScheduled.classList.toggle( 'bf-hidden',   isEmergency );

        blockScheduled.querySelectorAll( 'input, select, textarea' ).forEach( function ( el ) {
            el.disabled = isEmergency;
        } );

        modeToggle.querySelectorAll( '.bmt-btn' ).forEach( function ( btn ) {
            btn.classList.toggle( 'active', btn.dataset.mode === mode );
        } );

        if ( submitBtn ) submitBtn.className = isEmergency ? 'btn-emergency btn-full' : 'btn-primary btn-full';
        if ( btnText )   btnText.textContent  = isEmergency ? '🚀 Dispatch Technician Now' : '📅 Confirm Appointment';
    }

    if ( modeToggle ) {
        modeToggle.addEventListener( 'click', function ( e ) {
            var btn = e.target.closest( '.bmt-btn' );
            if ( btn && btn.dataset.mode !== currentMode ) {
                switchMode( btn.dataset.mode );
            }
        } );
    }

    // ── Price breakdown ───────────────────────────────────────────────────────
    var bookingSection = document.querySelector( '.fmtn-booking-section' );
    var depositAmt     = 0;

    if ( bookingSection ) {
        depositAmt = parseFloat( bookingSection.dataset.deposit ) || 0;
    }

    var elTotalRow  = document.getElementById( 'deposit-total-row' );
    var elTotalVal  = document.getElementById( 'deposit-total-val' );
    var elBalNote   = document.getElementById( 'deposit-balance-note' );
    var elBalVal    = document.getElementById( 'deposit-balance-val' );

    function showPriceBreakdown( servicePrice ) {
        if ( servicePrice && servicePrice > depositAmt ) {
            var balance = ( servicePrice - depositAmt ).toFixed( 2 );
            if ( elTotalRow ) elTotalRow.style.display = '';
            if ( elTotalVal ) elTotalVal.textContent   = '£' + parseFloat( servicePrice ).toFixed( 2 );
            if ( elBalNote  ) elBalNote.textContent    = 'Remaining balance due on the day';
            if ( elBalVal   ) elBalVal.textContent     = '£' + balance;
        } else {
            if ( elTotalRow ) elTotalRow.style.display = 'none';
            if ( elTotalVal ) elTotalVal.textContent   = '';
            if ( elBalNote  ) elBalNote.textContent    = 'Remaining balance due to technician on the day';
            if ( elBalVal   ) elBalVal.textContent     = '';
        }
    }

    function getPriceFromInput( input ) {
        return parseFloat( input.dataset.price ) || 0;
    }

    // Init: preselected service page
    if ( bookingSection && bookingSection.dataset.preselectedPrice ) {
        showPriceBreakdown( parseFloat( bookingSection.dataset.preselectedPrice ) );
    }

    // Init: first emergency radio is checked by default
    var firstRadio = form.querySelector( 'input[name="em_service"]:checked' );
    if ( firstRadio && getPriceFromInput( firstRadio ) ) {
        showPriceBreakdown( getPriceFromInput( firstRadio ) );
    }

    // ── Radio card highlight + price breakdown ────────────────────────────────
    form.addEventListener( 'change', function ( e ) {
        if ( e.target.name === 'em_service' ) {
            form.querySelectorAll( '.radio-card' ).forEach( function ( lbl ) {
                var inp = lbl.querySelector( 'input[type="radio"]' );
                lbl.classList.toggle( 'radio-card--active', inp && inp.checked );
            } );
            showPriceBreakdown( getPriceFromInput( e.target ) );
        }
    } );

    form.addEventListener( 'click', function ( e ) {
        var card = e.target.closest( '.radio-card' );
        if ( ! card ) return;
        var input = card.querySelector( 'input[type="radio"]' );
        if ( ! input ) return;
        input.checked = true;
        input.dispatchEvent( new Event( 'change', { bubbles: true } ) );
    } );

    // Scheduled service select
    var serviceSelect = document.getElementById( 'fmtn_service_select' );
    if ( serviceSelect ) {
        serviceSelect.addEventListener( 'change', function () {
            var opt = serviceSelect.options[ serviceSelect.selectedIndex ];
            showPriceBreakdown( opt ? parseFloat( opt.dataset.price ) : 0 );
        } );
    }

    // ── Detect location ───────────────────────────────────────────────────────
    const detectBtn     = document.getElementById( 'detect-location' );
    const detectStatus  = document.getElementById( 'detect-status' );
    const geoLat        = document.getElementById( 'geo_lat' );
    const geoLng        = document.getElementById( 'geo_lng' );
    const postcodeInput = form.querySelector( '#postcode' );

    if ( detectBtn ) {
        detectBtn.addEventListener( 'click', function () {
            if ( ! navigator.geolocation ) {
                setDetectStatus( 'Geolocation not supported — please enter your postcode manually.', 'error' );
                return;
            }
            detectBtn.disabled = true;
            setDetectStatus( 'Detecting your location…', 'pending' );

            navigator.geolocation.getCurrentPosition(
                function ( pos ) {
                    const lat = pos.coords.latitude.toFixed( 6 );
                    const lng = pos.coords.longitude.toFixed( 6 );
                    if ( geoLat ) geoLat.value = lat;
                    if ( geoLng ) geoLng.value = lng;
                    detectBtn.disabled = false;
                    setDetectStatus( '✓ Location captured — enter or confirm your postcode above.', 'ok' );

                    fetch(
                        'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + lat + '&lon=' + lng,
                        { headers: { 'Accept-Language': 'en-GB', 'User-Agent': 'FixMyTyreNow/1.0 (fixmytyrenow.com)' } }
                    )
                    .then( function ( r ) { return r.json(); } )
                    .then( function ( data ) {
                        const pc = data && data.address && ( data.address.postcode || '' );
                        if ( pc && postcodeInput ) {
                            postcodeInput.value = pc.trim().toUpperCase();
                            setDetectStatus( '✓ Postcode detected: ' + postcodeInput.value, 'ok' );
                        }
                    } )
                    .catch( function () {} );
                },
                function ( err ) {
                    detectBtn.disabled = false;
                    const msgs = {
                        1: 'Location access denied — please allow location access in your browser, or enter your postcode.',
                        2: 'Location unavailable — please enter your postcode manually.',
                        3: 'Location request timed out — please enter your postcode manually.',
                    };
                    setDetectStatus( msgs[ err.code ] || 'Could not detect location.', 'error' );
                },
                { timeout: 10000, maximumAge: 120000, enableHighAccuracy: false }
            );
        } );
    }

    function setDetectStatus( msg, type ) {
        if ( detectStatus ) {
            detectStatus.textContent = msg;
            detectStatus.className   = 'detect-status detect-' + type;
        }
    }

    // ── Helpers ───────────────────────────────────────────────────────────────
    function setLoading( loading ) {
        submitBtn.disabled    = loading;
        if ( btnText ) btnText.style.display = loading ? 'none'   : '';
        if ( btnLoad ) btnLoad.style.display = loading ? 'inline' : 'none';
    }

    function showMsg( text, type ) {
        if ( ! msgBox ) return;
        msgBox.textContent   = text;
        msgBox.className     = 'booking-msg booking-msg--' + type;
        msgBox.style.display = 'block';
        msgBox.scrollIntoView( { behavior: 'smooth', block: 'nearest' } );
    }

    function clearMsg() {
        if ( ! msgBox ) return;
        msgBox.textContent   = '';
        msgBox.style.display = 'none';
    }

    function showRevolutMsg( text, type ) {
        if ( ! revolutPayMsg ) return;
        revolutPayMsg.textContent   = text;
        revolutPayMsg.className     = 'booking-msg booking-msg--' + ( type || 'error' );
        revolutPayMsg.style.display = text ? 'block' : 'none';
    }

    function getField( name ) {
        const el = form.querySelector( '[name="' + name + '"]' );
        return el ? el.value.trim() : '';
    }

    function getServiceName() {
        const hidden = form.querySelector( 'input[type="hidden"][name="service_name"]' );
        if ( hidden ) return hidden.value;
        if ( currentMode === 'emergency' ) {
            const radio = form.querySelector( 'input[name="em_service"]:checked' );
            return radio ? radio.value : '';
        }
        return getField( 'sc_service' );
    }

    function validate() {
        if ( ! getField( 'customer_name' ) )  return 'Please enter your name.';
        if ( ! getField( 'customer_phone' ) ) return 'Please enter your phone number.';
        if ( ! getField( 'postcode' ) )       return 'Please enter your postcode or use Detect Location.';
        const email = getField( 'customer_email' );
        if ( ! email || ! email.includes( '@' ) ) return 'Please enter a valid email address.';
        if ( currentMode === 'scheduled' ) {
            if ( ! getField( 'booking_date' ) ) return 'Please select a preferred date.';
        }
        return null;
    }

    // ── State ─────────────────────────────────────────────────────────────────
    let bookingRef = '';
    let revolutId  = '';

    // ── Step 1: Submit booking ────────────────────────────────────────────────
    form.addEventListener( 'submit', async function ( e ) {
        e.preventDefault();
        clearMsg();

        const error = validate();
        if ( error ) { showMsg( error, 'error' ); return; }

        setLoading( true );

        const payload = {
            nonce:          config.nonce,
            booking_type:   currentMode,
            customer_name:  getField( 'customer_name' ),
            customer_email: getField( 'customer_email' ),
            customer_phone: getField( 'customer_phone' ),
            postcode:       getField( 'postcode' ).toUpperCase(),
            service_name:   getServiceName(),
            service_id:     getField( 'service_id' ),
            location_id:    getField( 'location_id' ),
            booking_date:   getField( 'booking_date' ),
            booking_slot:   getField( 'booking_slot' ),
            vehicle_reg:    getField( 'vehicle_reg' ).toUpperCase(),
            tyre_size:      getField( 'tyre_size' ),
            notes:          getField( 'notes' ),
            geo_lat:        getField( 'geo_lat' ),
            geo_lng:        getField( 'geo_lng' ),
        };

        let data;
        try {
            const res = await fetch( config.restUrl + 'book', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify( payload ),
            } );
            data = await res.json();
            if ( ! res.ok || data.error ) {
                showMsg( data.error || 'Booking failed. Please try again.', 'error' );
                setLoading( false );
                return;
            }
        } catch ( err ) {
            showMsg( 'Network error. Please check your connection and try again.', 'error' );
            setLoading( false );
            return;
        }

        bookingRef = data.booking_ref || '';
        revolutId  = data.revolut_id  || '';
        setLoading( false );

        if ( data.public_id ) {
            mountRevolutPayment( data.public_id, data.deposit, payload );
        } else {
            // Payment unavailable — show booking received + reason if any
            if ( data.revolut_error ) {
                showMsg( 'Payment could not be initialised (' + data.revolut_error + '). Your booking is saved — we will contact you to arrange payment.', 'error' );
            }
            showConfirmationNoPayment( payload, data );
        }
    } );

    // ── Step 2: Mount RevolutCheckout — payWithPopup (handles 3DS automatically)
    function mountRevolutPayment( publicId, deposit, payload ) {
        if ( submitWrap ) submitWrap.style.display = 'none';
        if ( revolutSection ) {
            revolutSection.style.display = 'block';
            revolutSection.scrollIntoView( { behavior: 'smooth', block: 'nearest' } );
        }

        if ( typeof RevolutCheckout === 'undefined' ) {
            showRevolutMsg( 'Payment widget failed to load. Please refresh and try again.', 'error' );
            return;
        }

        // Initialise the checkout instance once
        RevolutCheckout( publicId ).then( function ( instance ) {
            if ( ! revolutPayBtn ) return;

            revolutPayBtn.addEventListener( 'click', function () {
                setRevolutPayLoading( true );
                showRevolutMsg( '', '' );

                // payWithPopup opens Revolut's hosted UI — 3DS is handled inside the popup
                instance.payWithPopup( {
                    name:  payload.customer_name,
                    email: payload.customer_email,
                    onSuccess: function () {
                        confirmPayment( payload, deposit );
                    },
                    onError: function ( message ) {
                        setRevolutPayLoading( false );
                        showRevolutMsg( message || 'Payment failed. Please try again.', 'error' );
                    },
                    onCancel: function () {
                        setRevolutPayLoading( false );
                        showRevolutMsg( 'Payment cancelled — your booking is still saved.', 'error' );
                    },
                } );
            } );
        } ).catch( function () {
            showRevolutMsg( 'Could not initialise payment. Please refresh and try again.', 'error' );
        } );
    }

    function setRevolutPayLoading( loading ) {
        if ( ! revolutPayBtn ) return;
        revolutPayBtn.disabled = loading;
        const t = revolutPayBtn.querySelector( '.btn-text' );
        const l = revolutPayBtn.querySelector( '.btn-loading' );
        if ( t ) t.style.display = loading ? 'none'   : '';
        if ( l ) l.style.display = loading ? 'inline' : 'none';
    }

    // ── Step 3: Confirm payment server-side ───────────────────────────────────
    async function confirmPayment( payload, deposit ) {
        try {
            const res = await fetch( config.restUrl + 'confirm', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify( { nonce: config.nonce, revolut_id: revolutId } ),
            } );
            const data = await res.json();
            if ( ! res.ok || data.error ) {
                setRevolutPayLoading( false );
                showRevolutMsg( data.error || 'Could not confirm payment. Please contact us.', 'error' );
                return;
            }
        } catch ( err ) {
            setRevolutPayLoading( false );
            showRevolutMsg( 'Network error confirming payment. Please contact us.', 'error' );
            return;
        }
        showConfirmation( payload, deposit );
    }

    // ── Confirmation screen (deposit paid) ────────────────────────────────────
    function showConfirmation( payload, deposit ) {
        const section = form.closest( '.fmtn-booking-section' );
        if ( ! section ) return;
        const ref    = bookingRef || '—';
        const amount = deposit ? '£' + parseFloat( deposit ).toFixed( 2 ) : '£10.00';
        const eta    = payload.booking_type === 'emergency'
            ? '~20 minutes'
            : ( payload.booking_date || '' ) + ( payload.booking_slot ? ' · ' + payload.booking_slot : '' );
        const phone  = ( config.phone || '07340645595' ).replace( /\s/g, '' );

        section.innerHTML = [
            '<div class="booking-confirmation">',
            '  <div class="bc-icon">✅</div>',
            '  <h2 class="bc-title">Booking Confirmed!</h2>',
            '  <p class="bc-paid">Deposit of <strong>' + amount + '</strong> paid via Revolut</p>',
            payload.booking_type === 'emergency'
                ? '  <p class="bc-eta">A technician will be dispatched — estimated arrival <strong>' + eta + '</strong></p>'
                : '  <p class="bc-eta">Appointment booked for <strong>' + escHtml( eta ) + '</strong></p>',
            '  <div class="bc-details">',
            '    <div class="bc-row"><span>Service</span><strong>' + escHtml( payload.service_name || 'Tyre Fitting' ) + '</strong></div>',
            '    <div class="bc-row"><span>Location</span><strong>' + escHtml( payload.postcode ) + '</strong></div>',
            '    <div class="bc-row"><span>Reference</span><strong>' + escHtml( ref ) + '</strong></div>',
            '  </div>',
            '  <p class="bc-call">Need help? <a href="tel:' + escHtml( phone ) + '">Call us: ' + escHtml( config.phone || '07340 645595' ) + '</a></p>',
            '</div>',
        ].join( '\n' );
    }

    function showConfirmationNoPayment( payload, data ) {
        const section = form.closest( '.fmtn-booking-section' );
        if ( ! section ) return;
        const ref    = data.booking_ref || '—';
        const deposit = data.deposit ? '£' + parseFloat( data.deposit ).toFixed( 2 ) : '£10.00';
        const eta    = payload.booking_type === 'emergency'
            ? '~20 minutes'
            : ( payload.booking_date || '' ) + ( payload.booking_slot ? ' · ' + payload.booking_slot : '' );
        const phone  = ( config.phone || '07340645595' ).replace( /\s/g, '' );

        section.innerHTML = [
            '<div class="booking-confirmation">',
            '  <div class="bc-icon">✅</div>',
            '  <h2 class="bc-title">Booking Received!</h2>',
            payload.booking_type === 'emergency'
                ? '  <p class="bc-eta">A technician will be dispatched — estimated arrival <strong>' + eta + '</strong></p>'
                : '  <p class="bc-eta">Appointment booked for <strong>' + escHtml( eta ) + '</strong></p>',
            '  <div class="bc-details">',
            '    <div class="bc-row"><span>Service</span><strong>' + escHtml( payload.service_name || 'Tyre Fitting' ) + '</strong></div>',
            '    <div class="bc-row"><span>Location</span><strong>' + escHtml( payload.postcode ) + '</strong></div>',
            '    <div class="bc-row"><span>Reference</span><strong>' + escHtml( ref ) + '</strong></div>',
            '  </div>',
            '  <div class="bc-pay"><p class="bc-pay-note">Please pay the ' + deposit + ' deposit when our technician arrives.</p></div>',
            '  <p class="bc-call">Need help? <a href="tel:' + escHtml( phone ) + '">Call us: ' + escHtml( config.phone || '07340 645595' ) + '</a></p>',
            '</div>',
        ].join( '\n' );
    }

    function escHtml( str ) {
        return String( str || '' )
            .replace( /&/g, '&amp;' )
            .replace( /</g, '&lt;' )
            .replace( />/g, '&gt;' )
            .replace( /"/g, '&quot;' );
    }

} )();
