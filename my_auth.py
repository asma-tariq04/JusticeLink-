
import hashlib
import html

import streamlit as st


def is_logged_in():
    return bool(st.session_state.get("logged_in"))


def _start_session(username, email):
    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["name"] = username
    st.session_state["email"] = email
    return True, ""


def logout_user():
    for key in ("logged_in", "username", "name", "email", "after_login", "auth_message"):
        st.session_state.pop(key, None)
    st.session_state["current_screen"] = "home"

def login_user(username, password):
    username = (username or "").strip()
    if not username or not password:
        return False, "Please enter username and password."
   
    return _start_session(username, "")


def signup_user(username, email, password, confirm):
    username = (username or "").strip()
    email = (email or "").strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email."
    if len(password or "") < 8:
        return False, "Password must be at least 8 characters."
    if password != confirm:
        return False, "Passwords do not match."

    return _start_session(username, email)

def current_user_key():
    """Is user ke folder ke liye unique, safe ID (12 hex characters). Hamesha session se aati hai."""
    username = st.session_state.get("username")
    if not username:
        return None
    return hashlib.sha256(str(username).lower().encode("utf-8")).hexdigest()[:12]


def current_user_info():
    name = st.session_state.get("name") or st.session_state.get("username") or "User"
    email = st.session_state.get("email", "")
    return name, email


_PROFILE_CSS = """
<style>
.jl-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 20px 6px 25px;
    margin-top: 1.5rem;
    border-top: 1px solid #cfcac4;
}
.jl-avatar {
    width: 38px;
    height: 38px;
    min-width: 38px;
    border-radius: 50%;
    background: #594239;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 16px;
    font-family: "Century Gothic", sans-serif;
}
.jl-pname {
    font-family: "Century Gothic", sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #171717;
    line-height: 1.2;
}
.jl-pmail {
    font-family: "Century Gothic", sans-serif;
    font-size: 12px;
    color: #555555;
    word-break: break-all;
}
</style>
"""


def sidebar_profile():
    
    name, email = current_user_info()
    initial = html.escape(str(name)[:1].upper() or "?")

    card = '<div class="jl-profile"><div class="jl-avatar">' + initial + "</div><div>"
    card += '<div class="jl-pname">' + html.escape(str(name)) + "</div>"
    if email:
        card += '<div class="jl-pmail">' + html.escape(str(email)) + "</div>"
    card += "</div></div>"

    st.sidebar.markdown(_PROFILE_CSS, unsafe_allow_html=True)
    st.sidebar.markdown(card, unsafe_allow_html=True)

    if st.sidebar.button(
        "Logout",
        icon=":material/logout:",
        type="tertiary",
        width="stretch",
        key="jl_logout",
    ):
        logout_user()
        st.rerun()