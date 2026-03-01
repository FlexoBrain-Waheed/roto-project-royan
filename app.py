import streamlit as st, pandas as pd, io, plotly.express as px

st.set_page_config(page_title="Royan Plant - Roto", layout="wide")
st.title("🏭 Royan Smart Plant Simulator - Rotogravure Edition")

tabs = st.tabs(["1. Materials", "2. Production", "3. Consumables", "4. HR & OPEX", "5. Recipes (Roto)", "6. P&L & WC", "7. Offer"])

# --- TAB 1: Materials ---
with tabs[0]:
    st.markdown("### 📦 1. Ready Films & Foils (Bought in Rolls)")
    c1, c2, c3, c4 = st.columns(4)
    p_bopp_t = c1.number_input("BOPP Trans SAR", value=6.0, step=0.1)
    d_bopp_t = c1.number_input("BOPP Trans Den", value=0.91, step=0.01)
    
    p_bopp_p = c2.number_input("BOPP Pearl SAR", value=7.0, step=0.1)
    d_bopp_p = c2.number_input("BOPP Pearl Den", value=0.62, step=0.01)
    
    p_bopp_m = c3.number_input("BOPP Met SAR", value=6.3, step=0.1)
    d_bopp_m = c3.number_input("BOPP Met Den", value=0.91, step=0.01)
    
    p_pet = c4.number_input("PET SAR", value=6.3, step=0.1)
    d_pet = c4.number_input("PET Den", value=1.40, step=0.01)
    
    st.markdown("### 🧪 2. Specialized Films & Foils")
    c5, c6, c7 = st.columns(3)
    p_cpp = c5.number_input("CPP Film SAR (5800/Ton)", value=5.8, step=0.1)
    d_cpp = c5.number_input("CPP Den", value=0.91, step=0.01)
    
    p_al = c6.number_input("ALU Foil SAR", value=17.0, step=0.1)
    d_al = c6.number_input("ALU Den", value=2.70, step=0.01)
    
    p_pe_lam_film = c7.number_input("PE Lamination Film SAR", value=5.5, step=0.1)
    d_pe = c7.number_input("PE Density", value=0.92, step=0.01)
    
    mat_db = {
        "BOPP Trans": {"p": p_bopp_t, "d": d_bopp_t}, "BOPP Pearl": {"p": p_bopp_p, "d": d_bopp_p},
        "BOPP Met": {"p": p_bopp_m, "d": d_bopp_m}, "PET": {"p": p_pet, "d": d_pet},
        "CPP": {"p": p_cpp, "d": d_cpp}, "ALU": {"p": p_al, "d": d_al},
        "PE Lam Film": {"p": p_pe_lam_film, "d": d_pe}, "None": {"p": 0.0, "d": 0.0}
    }
    
    st.markdown("### 🎨 3. Chemicals & Adhesives")
    ci1, ci2, ci3 = st.columns(3)
    ink_p = ci1.number_input("Roto Ink/Kg", value=14.0, step=0.5)
    solv_p = ci2.number_input("Solvent/Kg", value=6.0, step=0.5)
    adh_p = ci3.number_input("Solvent-Based Adh/Kg", value=14.0, step=0.5)

# --- TAB 2: Production & Chart ---
with tabs[1]:
    cw1, cw2, cw3 = st.columns(3)
    d_yr = cw1.number_input("Days/Yr", value=300, step=1)
    s_day = cw1.number_input("Shifts/Day", value=2, step=1)
    h_sh = cw1.number_input("Hrs/Shift", value=12, step=1)
    j_mo = cw2.number_input("Jobs/Mo", value=50, step=1)
    c_hrs = cw2.number_input("C.O. Hrs", value=2.0, step=0.5) 
    kw_p = cw3.number_input("SAR/kWh", value=0.18, step=0.01)
    net_hrs = (d_yr * s_day * h_sh) - (j_mo * 12 * c_hrs)
    st.success(f"✅ Net Running Hours / Year: {net_hrs:,.0f}")
    
    st.markdown("### 1. Machine Parameters (Roto Specs)")
    m1, m2 = st.columns(2)
    with m1:
        r_s = st.number_input("Roto Speed m/min", value=400.0, step=10.0)
        r_w = st.number_input("Roto Width", value=1.0, step=0.1)
        r_e = st.slider("Roto Eff%", 1, 100, 80)
        r_k = st.number_input("Roto kW (Motors/Blowers only)", value=100.0, step=5.0)
        r_pr = st.number_input("Roto CAPEX", value=10500000.0, step=50000.0)
        r_lm_cap = net_hrs * 60.0 * r_s * (r_e/100.0)
    with m2:
        l_s = st.number_input("Lam Speed", value=400.0, step=10.0)
        l_w = st.number_input("Lam Width", value=1.0, step=0.1) 
        l_e = st.slider("Lam Eff%", 1, 100, 75)
        l_k = st.number_input("Lam kW (Motors/Blowers only)", value=50.0, step=5.0)
        l_pr = st.number_input("Lam CAPEX", value=2500000.0, step=50000.0)
        l_lm_cap = net_hrs * 60.0 * l_s * (l_e/100.0)
    
    m3, m4 = st.columns(2)
    with m3:
        s_s = st.number_input("Slit Speed", value=400.0, step=10.0)
        s_w = st.number_input("Slit Width", value=1.0, step=0.1) 
        s_e = st.slider("Slit Eff%", 1, 100, 50)
        s_k = st.number_input("Slit kW", value=40.0, step=5.0)
        s_pr = st.number_input("Slit CAPEX", value=800000.0, step=50000.0)
        s_lm_cap = net_hrs * 60.0 * s_s * (s_e/100.0)
    with m4:
        st.info("Bag Making is kept for Pouch/Bag formats.")
        b_q = st.number_input("Bag Mach Qty", value=3, step=1) 
        b_s = st.number_input("Bag Speed m/m", value=75.0, step=5.0)
        b_e = st.slider("Bag Eff%", 1, 100, 85)
        b_k = st.number_input("Bag kW Total", value=75.0, step=5.0)
        b_pr = st.number_input("Bag CAPEX", value=500000.0, step=50000.0)
        b_lm_cap = net_hrs * 60.0 * b_s * b_q * (b_e/100.0)

    st.markdown("### 2. Factory Utilities & Thermal Oil Boiler (غلاية الزيت)")
    u1, u2, u3, u4 = st.columns(4)
    blr_pr = u1.number_input("Boiler CAPEX", value=2500000.0, step=50000.0)
    blr_dep_y = u1.number_input("Boiler Depr Yrs", value=10.0, step=1.0)
    blr_lph = u2.number_input("Boiler Diesel L/hr", value=40.0, step=5.0)
    dsl_p = u2.number_input("Diesel Price SAR/L", value=1.79, step=0.05)
    
    chl_k = u3.number_input("Chiller kW", value=50.0, step=5.0)
    chl_pr = u3.number_input("Chiller CAPEX", value=500000.0, step=10000.0)
    cmp_k = u4.number_input("Compressor kW", value=30.0, step=5.0)
    cmp_pr = u4.number_input("Compressor CAPEX", value=250000.0, step=10000.0)

    hng_pr = st.number_input("Hangar CAPEX", value=4000000.0, step=50000.0)
    hng_dep_y = st.number_input("Hangar Depr Yrs", value=25.0, step=1.0)
    
    mac_dep_y = st.number_input("Machines Depreciation Yrs", value=10.0, step=1.0)
    dep_r, dep_l, dep_s, dep_b = r_pr/mac_dep_y, l_pr/mac_dep_y, s_pr/mac_dep_y, b_pr/mac_dep_y
    ann_dep = dep_r + dep_l + dep_s + dep_b + (hng_pr/hng_dep_y) + (chl_pr/10.0) + (cmp_pr/10.0) + (blr_pr/blr_dep_y)
    t_capex = r_pr + l_pr + s_pr + b_pr + hng_pr + chl_pr + cmp_pr + blr_pr

    st.markdown("### 📊 3. Machine Capacity Chart")
    chart_gsm = st.number_input("Avg GSM for Chart", value=40.0, step=1.0)
    df_cap = pd.DataFrame({
        "Machine": ["Roto Print", "Lam", "Slitter", "BagMk"],
        "Max Tons": [(r_lm_cap*r_w*chart_gsm/1000000), (l_lm_cap*l_w*chart_gsm/1000000), (s_lm_cap*s_w*chart_gsm/1000000), (b_lm_cap*chart_gsm/1000000)]
    })
    st.plotly_chart(px.bar(df_cap, x="Machine", y="Max Tons", color="Machine", text_auto='.0f'), use_container_width=True)

# --- TAB 3: Consumables (ROTO SPECIFIC) ---
with tabs[2]:
    st.subheader("🛠️ Consumables (Rotogravure Cylinders)")
    cc1, cc2 = st.columns(2)
    cyl_pr = cc1.number_input("Engraved Cylinder SAR/Color", value=1200.0, step=100.0)
    cyl_lf = cc1.number_input("Cylinder Life(m)", value=3000000.0, step=10000.0)
    avg_colors = cc1.number_input("Avg Colors per Job", value=6, step=1)
    
    bl_pr = cc2.number_input("Doctor Blade SAR/m", value=15.0, step=1.0)
    bl_qt = cc2.number_input("Blade m/Job", value=10.0, step=1.0)
    bl_lf = cc2.number_input("Blade Life(m)", value=150000.0, step=1000.0)

# --- TAB 4: HR & OPEX ---
with tabs[3]:
    st.header("🏢 HR & OPEX (الموارد البشرية والمصاريف الإدارية)")
    
    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown("**Production (Direct Labor)**")
        eng_q = st.number_input("Engineers Qty", value=3, step=1)
        eng_s = st.number_input("Engineer Salary", value=8000, step=500)
        opr_q = st.number_input("Operators Qty", value=6, step=1)
        opr_s = st.number_input("Operator Salary", value=4500, step=500)
        wrk_q = st.number_input("Workers Qty", value=10, step=1)
        wrk_s = st.number_input("Worker Salary", value=2500, step=500)
    with h2:
        st.markdown("**Admin & Support (Indirect)**")
        adm_q = st.number_input("Admin/Sales Qty", value=5, step=1)
        adm_s = st.number_input("Admin Salary", value=8000, step=500)
        sau_q = st.number_input("Saudi (Nitaqat) Qty", value=5, step=1)
        sau_s = st.number_input("Saudi Salary", value=4000, step=500)
    with h3:
        st.markdown("**Govt Fees & Benefits**")
        hidden_cost_pct = st.slider("Hidden Benefits % (Over Base Salary)", 0, 50, 20)

    st.markdown("#### 🏢 2. General & Admin Expenses (SG&A)")
    o1, o2, o3 = st.columns(3)
    rent_exp = o1.number_input("Land Rent & Licenses", value=8000, step=500)
    sales_exp = o1.number_input("Sales & Mktg", value=12000, step=500)
    it_exp = o2.number_input("IT & Software", value=5000, step=500)
    fac_exp = o2.number_input("Utilities & Maint.", value=5000, step=500)
    ins_exp = o3.number_input("Insurance", value=6000, step=500)
    misc_exp = o3.number_input("Consulting/Misc", value=4000, step=500)

    adm_exp = rent_exp + sales_exp + it_exp + fac_exp + ins_exp + misc_exp

    t_eng = eng_q * eng_s
    t_opr = opr_q * opr_s
    t_wrk = wrk_q * wrk_s
    t_adm = adm_q * adm_s
    t_sau = sau_q * sau_s
    
    base_payroll = t_eng + t_opr + t_wrk + t_adm + t_sau
    gov_benefits_cost = base_payroll * (hidden_cost_pct / 100.0)
    payroll = base_payroll + gov_benefits_cost 
    
    total_headcount = eng_q + opr_q + wrk_q + adm_q + sau_q
    saudization_pct = (sau_q / total_headcount) if total_headcount > 0 else 0
    
    st.markdown("---")
    st.markdown("#### 📊 HR & OPEX Dashboard")
    hm1, hm2, hm3, hm4 = st.columns(4)
    hm1.metric("👥 Total Headcount", f"{total_headcount} Emp")
    hm2.metric("🇸🇦 Saudization %", f"{saudization_pct:.1%}")
    hm3.metric("💸 Monthly Payroll", f"SAR {payroll:,.0f}")
    hm4.metric("🏢 Monthly Admin Exp", f"SAR {adm_exp:,.0f}")
    
    df_hr = pd.DataFrame({
        "Category": ["Engineers", "Operators", "Workers", "Admin", "Saudis", "Gov Fees/Benefits", 
                     "Rent & Licenses", "Sales & Mktg", "IT & Software", "Utilities & Maint", "Insurance", "Misc/Audit"],
        "Monthly Cost": [t_eng, t_opr, t_wrk, t_adm, t_sau, gov_benefits_cost, 
                         rent_exp, sales_exp, it_exp, fac_exp, ins_exp, misc_exp]
    })
    df_hr = df_hr[df_hr["Monthly Cost"] > 0]
    
    st.plotly_chart(px.pie(df_hr, names="Category", values="Monthly Cost", title="Total Monthly OPEX Breakdown", hole=0.4), use_container_width=True)

# --- TAB 5: Recipes & Detailed Costing (ROTO FFS & 3-LAYER POUCHES) ---
with tabs[4]:
    st.markdown("### ⚙️ 1. Global Production Settings (Roto)")
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    t_tons = c_s1.number_input("🎯 Target Tons", value=4500.0, step=100.0)
    std_w = c_s2.number_input("📏 Web Width (m)", value=1.000, step=0.1)
    w_ink = c_s3.number_input("🎨 Wet Ink (GSM)", value=6.0, step=0.1) 
    i_loss = c_s4.number_input("💧 Ink Loss %", value=50.0, step=1.0) 
    
    st.markdown("#### 🧪 Chemical Ratios (نسب الخلط)")
    c_r1, c_r2, c_r3 = st.columns(3)
    roto_solv_ratio = c_r1.number_input("Roto Solvent Ratio (Solvent/Ink)", value=2.0, step=0.1, help="2.0 means 1 kg ink requires 2 kg solvent")
    a_gsm = c_r2.number_input("🍯 Adh GSM (Solvent Base)", value=2.5, step=0.1)
    lam_solv_ratio = c_r3.number_input("Lam Solvent Ratio (Solvent to Adhesive %)", value=40.0, step=5.0)
    
    d_ink = w_ink * (1.0 - (i_loss/100.0))
    
    st.markdown("### ♻️ 2. Scrap Engine")
    cw1, cw2, cw3, cw4 = st.columns(4)
    w_flx = cw1.number_input("Roto Waste %", value=4.0, step=0.5) 
    w_lam = cw2.number_input("Lam Waste %", value=1.5, step=0.5)
    w_fin = cw3.number_input("Finishing Waste %", value=1.5, step=0.5)
    scrap_p = cw4.number_input("Scrap Resale (SAR/Kg)", value=1.5, step=0.1)
    
    st.markdown("### 📋 3. Smart Product Portfolio (3-Layer Supported)")
    # 🌟 التعديل: تغيير Format ليكون Bag بدلاً من Roll ليمر على تقطيع الأكياس مباشرة 🌟
    init_data = [
        {"Product": "1 Lyr BOPP Trans", "Format": "Roll (Slitted)", "Print": True, "L1": "BOPP Trans", "M1": 35, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 10, "Price": 13.0},
        {"Product": "1 Lyr BOPP Pearl", "Format": "Roll (Slitted)", "Print": True, "L1": "BOPP Pearl", "M1": 38, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 10, "Price": 13.5},
        {"Product": "1 Lyr CPP Bread Bag", "Format": "Bag", "Print": True, "L1": "CPP", "M1": 30, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 10, "Price": 17.0},
        {"Product": "2 Lyr PE + PE", "Format": "Roll (Slitted)", "Print": True, "L1": "PE Lam Film", "M1": 40, "L2": "PE Lam Film", "M2": 50, "L3": "None", "M3": 0, "Mix%": 10, "Price": 11.0},
        {"Product": "2 Lyr PET + PE", "Format": "Roll (Slitted)", "Print": True, "L1": "PET", "M1": 12, "L2": "PE Lam Film", "M2": 50, "L3": "None", "M3": 0, "Mix%": 10, "Price": 13.5},
        {"Product": "2 Lyr BOPP + Met", "Format": "Roll (Slitted)", "Print": True, "L1": "BOPP Trans", "M1": 20, "L2": "BOPP Met", "M2": 20, "L3": "None", "M3": 0, "Mix%": 10, "Price": 13.5},
        {"Product": "2 Lyr BOPP + BOPP", "Format": "Roll (Slitted)", "Print": True, "L1": "BOPP Trans", "M1": 20, "L2": "BOPP Trans", "M2": 20, "L3": "None", "M3": 0, "Mix%": 16, "Price": 13.5},
        {"Product": "Stand-up pouches 3 Lyr", "Format": "Bag", "Print": True, "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE Lam Film", "M3": 50, "Mix%": 24, "Price": 18.0}
    ]
    
    df_rec = st.data_editor(
        pd.DataFrame(init_data), 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Format": st.column_config.SelectboxColumn(
                "Format", options=["Roll (Slitted)", "Jumbo Roll", "Bag"], required=True
            )
        }
    )
    
    total_mix = df_rec["Mix%"].sum()
    if total_mix == 100:
        st.success(f"✅ Total Mix: **{total_mix}%** (Perfect Allocation)")
    else:
        st.error(f"⚠️ Total Mix: **{total_mix}%** (Please adjust the table above so the sum is exactly 100%)")
    
    w_gsm, t_roto_lm, t_lam_sqm, tons_flx, tons_lam, tons_slt, tons_bag = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    t_slt_lm, temp_dets = 0.0, []
    t_ink_k, t_slv_k, t_adh_k = 0.0, 0.0, 0.0
    
    for _, r in df_rec.iterrows():
        is_p, r_ton = r.get("Print", True), t_tons*(r.get("Mix%", 0)/100.0)
        
        m1, m2, m3 = float(r.get("M1", 0)), float(r.get("M2", 0)), float(r.get("M3", 0))
        l1, l2, l3 = str(r.get("L1", "None")), str(r.get("L2", "None")), str(r.get("L3", "None"))
        
        lp = (1 if m2 > 0 and l2 != "None" else 0) + (1 if m3 > 0 and l3 != "None" else 0)
        
        u_slt = r.get("Format") == "Roll (Slitted)"
        u_bag = r.get("Format") == "Bag"
        
        y = 1.0
        if is_p: y *= (1.0 - w_flx/100.0)
        if lp > 0: y *= (1.0 - w_lam/100.0)**lp
        if u_slt or u_bag: y *= (1.0 - w_fin/100.0)
        
        gross_ton = r_ton / y if y > 0 else r_ton
        
        if is_p: tons_flx += gross_ton
        if lp > 0: tons_lam += (gross_ton * lp) 
        if u_slt: tons_slt += gross_ton
        if u_bag: tons_bag += gross_ton
        
        g1 = m1 * mat_db.get(l1, {"d": 0})["d"]
        g2 = m2 * mat_db.get(l2, {"d": 0})["d"]
        g3 = m3 * mat_db.get(l3, {"d": 0})["d"]
        
        tg = g1 + g2 + g3 + (lp*a_gsm) + (d_ink if is_p else 0)
        
        p1 = mat_db.get(l1, {"p": 0})["p"]
        p2 = mat_db.get(l2, {"p": 0})["p"]
        p3 = mat_db.get(l3, {"p": 0})["p"]
        
        c_mat_ideal = ((g1/1000*p1) + (g2/1000*p2) + (g3/1000*p3) + 
                       (lp*a_gsm/1000*adh_p) + (lp*a_gsm*(lam_solv_ratio/100.0)/1000*solv_p) + 
                       (w_ink/1000*ink_p if is_p else 0) + 
                       (w_ink*roto_solv_ratio/1000*solv_p if is_p else 0)) / (tg/1000.0) if tg>0 else 0
        
        gross_mat_cost = c_mat_ideal / y if y > 0 else c_mat_ideal
        scrap_rev_kg = ((1.0/y) - 1.0) * scrap_p if y > 0 else 0
        net_mat_cost = gross_mat_cost - scrap_rev_kg
        
        l_len = (r_ton*1000000/tg)/std_w if tg>0 and std_w>0 else 0
        gross_len = l_len / y if y > 0 else l_len
        
        if is_p: 
            t_roto_lm += gross_len
            t_ink_k += (gross_len * std_w * w_ink) / 1000.0
            t_slv_k += (gross_len * std_w * w_ink * roto_solv_ratio) / 1000.0
        if lp > 0: 
            t_lam_sqm += (gross_len*std_w*lp)
            t_adh_k += (gross_len * std_w * a_gsm * lp) / 1000.0
            t_slv_k += (gross_len * std_w * a_gsm * (lam_solv_ratio/100.0) * lp) / 1000.0 
        if u_slt: t_slt_lm += gross_len
        w_gsm += tg*(r.get("Mix%", 0)/100.0)
        
        temp_dets.append({
            "Product":r["Product"], "Format":r["Format"], "Tons":r_ton, "GSM":tg, 
            "GrossMatCost":gross_mat_cost, "NetMatCost":net_mat_cost, 
            "Waste%": (1-y), "ScrapRev/Kg": scrap_rev_kg, "Price":r["Price"], 
            "lp":lp, "u_slt":u_slt, "u_bag":u_bag, "is_p": is_p
        })

    ln_m = (t_tons*1000/w_gsm*1000)/std_w if w_gsm>0 and std_w>0 else 0
    a_cons = ((t_roto_lm/cyl_lf)*cyl_pr*avg_colors if cyl_lf>0 else 0) + ((ln_m/bl_lf)*bl_qt*bl_pr if bl_lf>0 else 0)
    
    rr_h, rl_h = t_roto_lm/(r_s*60*(r_e/100)) if r_s*r_e>0 else 0, (t_lam_sqm/std_w)/(l_s*60*(l_e/100)) if l_s*l_e*std_w>0 else 0
    rs_h, rb_h = t_slt_lm/(s_s*60*(s_e/100)) if s_s*s_e>0 else 0, tons_bag/(b_s*60*b_q*(b_e/100)*std_w/1000) if tons_bag>0 and b_s*b_q*b_e>0 else 0
    
    pr, pl, ps, pb = rr_h*r_k*kw_p + dep_r + a_cons, rl_h*l_k*kw_p + dep_l, rs_h*s_k*kw_p + dep_s, rb_h*b_k*kw_p + dep_b
    po = (payroll+adm_exp)*12 + (hng_pr/25) + (chl_pr/10) + (cmp_pr/10) + (blr_pr/blr_dep_y) + (net_hrs*(chl_k+cmp_k)*kw_p) + (net_hrs*blr_lph*dsl_p)
    r_r, r_l, r_s, r_b, r_o = pr/(tons_flx*1000) if tons_flx>0 else 0, pl/(tons_lam*1000) if tons_lam>0 else 0, ps/(tons_slt*1000) if tons_slt>0 else 0, pb/(tons_bag*1000) if tons_bag>0 else 0, po/(t_tons*1000) if t_tons>0 else 0

    dets = []
    for d in temp_dets:
        c_r = r_r if d["is_p"] else 0
        c_l = r_l * d["lp"]
        c_s = r_s if d["u_slt"] else 0
        c_b = r_b if d["u_bag"] else 0
        t_cost = d["NetMatCost"] + c_r + c_l + c_s + c_b + r_o
        m_pct = (d["Price"] - t_cost) / d["Price"] if d["Price"] > 0 else 0
        
        dets.append({
            "Product": d["Product"], "Format": d["Format"], "Tons": d["Tons"], "Waste%": d["Waste%"], "NetMatCost": d["NetMatCost"], 
            "Roto Print": c_r, "Lam": c_l, "Slit": c_s, "BagMk": c_b, "OH": r_o,
            "TotalCost": t_cost, "Price": d["Price"], "Profit": d["Price"]-t_cost, "Margin%": m_pct, "GSM": d["GSM"], "GrossMatCost": d["GrossMatCost"], "ScrapRev/Kg": d["ScrapRev/Kg"]
        })
    
    st.markdown("### 📊 4. Detailed ABC Costing & Margins (SAR/Kg)")
    df_show = pd.DataFrame(dets)
    
    def color_negative_red(val):
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'
        
    format_dict = {
        "Tons": "{:,.1f}", "Waste%": "{:,.1%}", "NetMatCost": "{:,.2f}", "Roto Print": "{:,.2f}", 
        "Lam": "{:,.2f}", "Slit": "{:,.2f}", "BagMk": "{:,.2f}", "OH": "{:,.2f}", 
        "TotalCost": "{:,.2f}", "Price": "{:,.2f}", "Profit": "{:,.2f}", "Margin%": "{:,.2%}"
    }
    st.dataframe(df_show[["Product", "Format", "Tons", "Waste%", "NetMatCost", "Roto Print", "Lam", "Slit", "BagMk", "OH", "TotalCost", "Price", "Profit", "Margin%"]].style.format(format_dict).map(color_negative_red, subset=['Profit', 'Margin%']), use_container_width=True)

    st.markdown("### 🥧 5. Cost Structure Breakdown")
    df_melt = df_show.melt(id_vars="Product", value_vars=["NetMatCost", "Roto Print", "Lam", "Slit", "BagMk", "OH"], var_name="Cost Component", value_name="Cost (SAR/Kg)")
    st.plotly_chart(px.bar(df_melt, x="Product", y="Cost (SAR/Kg)", color="Cost Component", title="Where does the money go?", text_auto=".2f"), use_container_width=True)

    st.markdown("### 🚦 6. Line Balancing (Bottleneck Check)")
    cb1, cb2, cb3, cb4 = st.columns(4)
    
    if t_roto_lm <= r_lm_cap: cb1.success(f"Roto (M m)\n\nCap: {r_lm_cap/1000000:,.2f}\n\nReq: {t_roto_lm/1000000:,.2f}")
    else: cb1.error(f"Roto (M m)\n\nCap: {r_lm_cap/1000000:,.2f}\n\nReq: {t_roto_lm/1000000:,.2f}")
    
    if (t_lam_sqm/std_w if std_w>0 else 0) <= l_lm_cap: cb2.success(f"Lam (M m)\n\nCap: {l_lm_cap/1000000:,.2f}\n\nReq: {(t_lam_sqm/std_w if std_w>0 else 0)/1000000:,.2f}")
    else: cb2.error(f"Lam (M m)\n\nCap: {l_lm_cap/1000000:,.2f}\n\nReq: {(t_lam_sqm/std_w if std_w>0 else 0)/1000000:,.2f}")

    if t_slt_lm <= s_lm_cap: cb3.success(f"Slit (M m)\n\nCap: {s_lm_cap/1000000:,.2f}\n\nReq: {t_slt_lm/1000000:,.2f}")
    else: cb3.error(f"Slit (M m)\n\nCap: {s_lm_cap/1000000:,.2f}\n\nReq: {t_slt_lm/1000000:,.2f}")
    
    if tons_bag <= b_lm_cap: cb4.success(f"BagMk (M m)\n\nCap: {b_lm_cap/1000000:,.2f}\n\nReq: {tons_bag/1000000:,.2f}")
    else: cb4.error(f"BagMk (M m)\n\nCap: {b_lm_cap/1000000:,.2f}\n\nReq: {tons_bag/1000000:,.2f}")

# --- TAB 6 & 7: P&L Summary & SMART EXCEL EXPORT ---
with tabs[5]:
    total_rev = sum(d['Price']*d['Tons']*1000 for d in dets)
    total_scrap_rev = sum(d['ScrapRev/Kg']*d['Tons']*1000 for d in dets)
    total_all_cost = sum(d['TotalCost']*d['Tons']*1000 for d in dets)
    total_gross_mat = sum(d['GrossMatCost']*d['Tons']*1000 for d in dets)
    cash_opex = total_all_cost - ann_dep - total_gross_mat + total_scrap_rev
    
    net_profit_before_tax = total_rev - total_all_cost

    st.markdown("### 🏛️ Ownership & Tax (هيكل الملكية والضرائب)")
    corp_tax = net_profit_before_tax * 0.20 if net_profit_before_tax > 0 else 0
    net_profit_after_tax = net_profit_before_tax - corp_tax
    
    st.info(f"الاستثمار أجنبي 100% (MISA): يخضع المشروع لـ 20% ضريبة دخل للشركات على صافي الأرباح.")
    st.error(f"💸 **مبلغ الضريبة المستحق الدفع (20% Corporate Tax):** SAR {corp_tax:,.0f}")

    st.markdown("---")
    st.markdown("### ⏳ Working Capital Cycle (دورة رأس المال العامل)")
    wc_c1, wc_c2, wc_c3 = st.columns(3)
    ar_days = wc_c1.number_input("Receivable Days", value=60, step=15)
    inv_days = wc_c2.number_input("Inventory Days", value=45, step=15)
    ap_days = wc_c3.number_input("Payable Days", value=30, step=15)

    receivables = (total_rev / 365.0) * ar_days
    inventory = ((total_gross_mat + cash_opex) / 365.0) * inv_days
    payables = (total_gross_mat / 365.0) * ap_days
    working_capital = receivables + inventory - payables
    total_investment = t_capex + working_capital
    
    roi_pct = (net_profit_after_tax / total_investment) if total_investment > 0 else 0
    payback_yrs = (total_investment / net_profit_after_tax) if net_profit_after_tax > 0 else 0
    net_margin = (net_profit_after_tax / total_rev) if total_rev > 0 else 0
    
    wc_m1, wc_m2, wc_m3, wc_m4 = st.columns(4)
    wc_m1.metric("Cash with Customers", f"SAR {receivables:,.0f}")
    wc_m2.metric("Cash in Inventory", f"SAR {inventory:,.0f}")
    wc_m3.metric("Supplier Credit", f"SAR {payables:,.0f}")
    wc_m4.metric("💰 Required WC", f"SAR {working_capital:,.0f}")
    
    st.markdown("---")
    st.header("📈 Plant Financial Summary & Investor KPIs")
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Revenue", f"SAR {total_rev:,.0f}")
    f2.metric("Total Cost", f"SAR {total_all_cost:,.0f}")
    f3.metric("Corporate Tax (20%)", f"SAR {corp_tax:,.0f}")
    f4.metric("Net Profit (After Tax)", f"SAR {net_profit_after_tax:,.0f}")
    
    st.warning(f"🏦 **Total Initial Investment Required:** SAR {total_investment:,.0f} *(CAPEX: {t_capex:,.0f} + Working Capital: {working_capital:,.0f})*")
    
    k1, k2, k3 = st.columns(3)
    k1.info(f"**ROI (العائد على الاستثمار):** {roi_pct:.1%}")
    k2.info(f"**Payback Period (فترة الاسترداد):** {payback_yrs:.1f} Years")
    k3.info(f"**Net Profit Margin (هامش الربح الصافي):** {net_margin:.1%}")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        wb = w.book
        h_fmt = wb.add_format({'bold': True, 'bg_color': '#0f4c81', 'font_color': 'white', 'border': 1, 'align': 'center'})
        n_fmt = wb.add_format({'num_format': '#,##0.00', 'border': 1})
        p_fmt = wb.add_format({'num_format': '0.00%', 'border': 1})
        title_fmt = wb.add_format({'bold': True, 'font_size': 14, 'bg_color': '#e2efda', 'align': 'center', 'border': 1})
        
        df_mat_export = pd.DataFrame([{"المادة الخام": k, "السعر (ريال/كجم)": v["p"], "الكثافة": v["d"]} for k, v in mat_db.items() if k != "None"])
        df_mat_export.to_excel(w, sheet_name='1. المواد الخام', index=False)
        w.sheets['1. المواد الخام'].set_column('A:C', 20)
        
        df_mac_export = pd.DataFrame({
            "الماكينة": ["طباعة روتو", "لامنيشن", "قص (سلتر)", "تشكيل أكياس", "غلاية زيت حراري"],
            "قيمة الاستثمار CAPEX (ريال)": [r_pr, l_pr, s_pr, b_pr, blr_pr]
        })
        df_mac_export.to_excel(w, sheet_name='2. الماكينات والإنتاج', index=False)
        w.sheets['2. الماكينات والإنتاج'].set_column('A:B', 25)
        
        df_hr_export = df_hr.rename(columns={"Category": "البند", "Monthly Cost": "التكلفة الشهرية (ريال)"})
        df_hr_export["التكلفة السنوية (ريال)"] = df_hr_export["التكلفة الشهرية (ريال)"] * 12
        df_hr_export.to_excel(w, sheet_name='3. الموارد البشرية والتشغيل', index=False)
        w.sheets['3. الموارد البشرية والتشغيل'].set_column('A:C', 25)
        
        df_costing = df_show.drop(columns=['GSM', 'GrossMatCost']).rename(columns={
            "Product": "المنتج", "Format": "الشكل", "Tons": "الكمية (طن)", "Waste%": "نسبة الهالك",
            "NetMatCost": "المواد", "Roto Print": "طباعة", "Lam": "لامنيشن", 
            "Slit": "قص", "BagMk": "تشكيل", "OH": "إدارة", "TotalCost": "إجمالي التكلفة", 
            "Price": "سعر البيع", "Profit": "الربح/كجم", "Margin%": "هامش الربح", "ScrapRev/Kg": "عائد السكراب"
        })
        df_costing.to_excel(w, sheet_name='4. تحليل التكاليف', index=False)
        w.sheets['4. تحليل التكاليف'].set_column('A:O', 15)
        
        ws_inv = wb.add_worksheet('5. الملخص المالي للمستثمر')
        ws_inv.set_column('A:B', 30)
        ws_inv.merge_range('A1:B1', 'دراسة الجدوى - الملخص المالي (Royan Roto Plant)', title_fmt)
        ws_inv.write('A3', 'إجمالي الاستثمار في الأصول (CAPEX)', h_fmt)
        ws_inv.write('B3', t_capex, n_fmt)
        ws_inv.write('A4', 'رأس المال العامل المطلوب (Working Capital)', h_fmt)
        ws_inv.write('B4', working_capital, n_fmt)
        ws_inv.write('A5', 'إجمالي الاستثمار المطلوب لبدء المشروع', h_fmt)
        ws_inv.write('B5', total_investment, n_fmt)
        
        ws_inv.write('A7', 'الإيرادات السنوية (المبيعات)', h_fmt)
        ws_inv.write('B7', total_rev, n_fmt)
        ws_inv.write('A8', 'الإيرادات السنوية (استرداد السكراب)', h_fmt)
        ws_inv.write('B8', total_scrap_rev, n_fmt)
        ws_inv.write('A9', 'إجمالي التكاليف السنوية (شاملة الإهلاك والديزل)', h_fmt)
        ws_inv.write('B9', total_all_cost, n_fmt)
        ws_inv.write('A10', 'صافي الربح قبل الضرائب', h_fmt)
        ws_inv.write('B10', net_profit_before_tax, n_fmt)
        
        ws_inv.write('A12', 'ضريبة الاستثمار الأجنبي (Corporate Tax 20%)', h_fmt)
        ws_inv.write('B12', corp_tax, n_fmt)
        ws_inv.write('A13', 'صافي الربح النهائي (Net Profit After Tax)', h_fmt)
        ws_inv.write('B13', net_profit_after_tax, n_fmt)
        
        ws_inv.merge_range('A15:B15', 'المؤشرات المالية (Financial KPIs)', title_fmt)
        ws_inv.write('A16', 'هامش الربح الصافي (Net Margin %)', h_fmt)
        ws_inv.write('B16', net_margin, p_fmt)
        ws_inv.write('A17', 'العائد على الاستثمار (ROI %)', h_fmt)
        ws_inv.write('B17', roi_pct, p_fmt)
        ws_inv.write('A18', 'فترة استرداد رأس المال (بالسنوات)', h_fmt)
        ws_inv.write('B18', payback_yrs, n_fmt)

    st.download_button("📥 Download Roto Master Excel Study (Arabic)", buf.getvalue(), "Royan_Roto_Master_Study_Arabic.xlsx", use_container_width=True)

with tabs[6]:
    st.header("Commercial Offer")
    sr = st.selectbox("Select Product", [d['Product'] for d in dets])
    row = next(i for i in dets if i["Product"] == sr)
    if st.button("Generate"):
        st.info(f"**Customer:** Valued Client\n\n**Product:** {row['Product']} ({row['GSM']:,.1f} g/m²)\n\n**Format:** {row['Format']}\n\n**Price:** SAR {row['Price']:,.2f} / Kg\n\n*Waheed Waleed Malik, Royan*")
