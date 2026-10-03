import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SmartShop",
    page_icon="🛒",
    layout="wide"
)

# ================= GLOBAL CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Sidebar logo box */
.sidebar-logo {
    background:#161b22;
    padding:18px;
    border-radius:14px;
    text-align:center;
    margin-bottom:20px;
}

/* Amazon buttons */
div.stButton > button {
    background-color:#f0c14b;
    color:black;
    border-radius:8px;
    font-weight:600;
    height:42px;
}

/* Product card */
.product-card {
    background:#161b22;
    padding:16px;
    border-radius:16px;
}

/* Fixed image size */
.product-image {
    width:100%;
    height:230px;
    object-fit:cover;
    border-radius:12px;
    margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
def init_state():
    defaults = {
        "logged_in": False,
        "otp": None,
        "page": "shop",
        "cart": [],
        "wishlist": []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ================= LOGIN =================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        st.markdown("## 🔐 Login to SmartShop")
        with st.container(border=True):
            phone = st.text_input("📱 Mobile Number")
            if st.button("Send OTP"):
                if phone.isdigit() and len(phone) == 10:
                    st.session_state.otp = random.randint(1000,9999)
                    st.success(f"OTP Sent (Demo: {st.session_state.otp})")
                else:
                    st.error("Invalid number")

            if st.session_state.otp:
                otp = st.text_input("Enter OTP")
                if st.button("Verify & Login"):
                    if otp.isdigit() and int(otp) == st.session_state.otp:
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Wrong OTP")
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h1 style="margin:0;">🛒 SmartShop</h1>
        <p style="margin:4px 0 0;color:#9da5b4;">
            Professional E-Commerce App
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.success("Logged in")

    if st.button("🛍️ Shop", use_container_width=True):
        st.session_state.page = "shop"
    if st.button("❤️ Wishlist", use_container_width=True):
        st.session_state.page = "wishlist"
    if st.button("🧾 Checkout", use_container_width=True):
        st.session_state.page = "checkout"

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ================= PRODUCT DATA =================
products = pd.DataFrame({
    "Item": [
        "White Sleeve Top",
        "AI Book",
        "Backpack",
        "Shoes",
        "Fruits Pack",
        "Remote Car",
        "Lego Set",
        "Electric Scooter"
    ],
    "Price": [
        1100, 25000, 799, 1999, 299, 1499, 1999, 85000
    ],
    "Image": [
        "https://static.cilory.com/796564-thickbox_default/white-georgette-balloon-sleeves-casual-top.jpg.webp",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSBWSmlYAVmaUCqv9YIHX5UC5SGPMPlFmvVQ&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfpE059ajHKaGuhe9JYspE7Lhr9Mh-EXtsoQ&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8gT9Xj31IQWzissipIqKwQ6IPgaVbaxpylQ&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0zhWHY3Ltmps5_46bRaAiBMwMYEJG7hVNojKd8QhZvg&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCtNwanU5KBFHTItU1KxHb-0KYm3Z1d5FV_Q&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZqznssQlOYLkLLyA6GJqAMC6e4en8XSRD2A&s",
        "data:image/jpeg;base64,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"
    ]
})

# ================= SHOP =================
if st.session_state.page == "shop":
    st.markdown("## 🛍️ Products")
    cols = st.columns(3, gap="large")

    for i, row in products.iterrows():
        with cols[i % 3]:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown(
                f"<img src='{row['Image']}' class='product-image'>",
                unsafe_allow_html=True
            )
            st.subheader(row["Item"])
            st.caption(f"₹ {row['Price']:,}")

            qty = st.number_input("Quantity", 0, 5, 0, key=f"qty_{i}")

            if st.button("Add to Cart", key=f"cart_{i}"):
                if qty > 0:
                    st.session_state.cart.append({
                        "Item": row["Item"],
                        "Qty": qty,
                        "Total": qty * row["Price"]
                    })
                    st.success("Added")

            if st.button("❤️ Wishlist", key=f"wish_{i}"):
                if row["Item"] not in st.session_state.wishlist:
                    st.session_state.wishlist.append(row["Item"])
                    st.success("Wishlisted")

            st.markdown("</div>", unsafe_allow_html=True)

# ================= WISHLIST =================
if st.session_state.page == "wishlist":
    st.markdown("## ❤️ Wishlist")
    if not st.session_state.wishlist:
        st.info("Wishlist empty")
    else:
        for i, item in enumerate(st.session_state.wishlist):
            col1, col2 = st.columns([4,1])
            col1.write(item)
            if col2.button("❌ Remove", key=f"rw_{i}"):
                st.session_state.wishlist.pop(i)
                st.rerun()

# ================= CHECKOUT =================
if st.session_state.page == "checkout":
    st.markdown("## 🧾 Checkout")

    if not st.session_state.cart:
        st.warning("Cart empty")
    else:
        df = pd.DataFrame(st.session_state.cart)
        st.dataframe(df, use_container_width=True)

        total = df["Total"].sum()
        gst = total * 0.18
        final = total + gst

        st.metric("Total Payable", f"₹ {final:,.0f}")

        if st.button("💳 Pay Now"):
            with st.spinner("Processing payment..."):
                time.sleep(1)
            st.balloons()
            st.success("Payment Successful 🎉")
st.markdown(" Made with AI student By Streamlit ❤️")