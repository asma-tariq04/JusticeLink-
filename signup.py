

from pathlib import Path
from responsive import apply_responsive
import streamlit as st
import streamlit.components.v1 as components

from my_auth import login_user, signup_user

_FORM_DIR = Path(__file__).parent / "auth_form"
_auth_form = components.declare_component("jl_auth_form", path=str(_FORM_DIR))

_CSS = """
<style>
[data-testid="stMainBlockContainer"] {
    padding-top: 0.5rem !important;
    margin-top: 0rem !important;
}
[data-testid="stVerticalBlock"] { gap: 0rem !important; }
iframe {
    border: none !important;
    background: transparent !important;
    width: 100% !important;
}
</style>
"""


def _handle(result):
   
    nonce = result.get("nonce")
    
    if not nonce or nonce == st.session_state.get("last_auth_nonce"):
        return
    st.session_state["last_auth_nonce"] = nonce

    event = result.get("event")
    if event == "login":
        ok, text = login_user(result.get("username", ""), result.get("password", ""))
    elif event == "signup":
        ok, text = signup_user(
            result.get("username", ""),
            result.get("email", ""),
            result.get("password", ""),
            result.get("confirm", ""),
        )
    else:
        return

    if ok:
        st.session_state.pop("auth_message", None)
        st.session_state["current_screen"] = st.session_state.pop("after_login", "home")
        st.rerun()

    st.session_state["auth_message"] = {"text": text, "type": "error", "target": event}
    st.rerun()


def run():
    apply_responsive()
    st.markdown(_CSS, unsafe_allow_html=True)

    msg = st.session_state.get("auth_message") or {}
    result = _auth_form(
        message=msg.get("text", ""),
        message_type=msg.get("type", "error"),
        message_target=msg.get("target", "login"),
        key="jl_auth_form",
        default=None,
    )

    if result:
        _handle(result)

