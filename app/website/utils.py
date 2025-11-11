import time
import streamlit as st

def init_session_state():
    """Инициализация состояния сессии"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        from agent_mock import DialogAgent
        st.session_state.agent = DialogAgent()

def render_sidebar(auth_manager):
    """Отрисовка сайдбара"""
    with st.sidebar:
        st.title(f"🤖 Привет, {st.session_state.username}!")
        st.markdown("---")
        
        # Информация о системе
        stats = auth_manager.get_system_stats()
        st.markdown("**Информация о системе:**")
        st.markdown(f"Пользователей: {stats['total_users']}")
        st.markdown(f"Активных сессий: {stats['active_sessions']}")
        
        st.markdown("---")
        
        if st.button("Выйти"):
            auth_manager.logout_user()
            st.rerun()
        
        st.markdown("---")
        if st.button("Очистить историю"):
            st.session_state.messages = [
                {"role": "assistant", "content": "История очищена. Чем могу помочь?"}
            ]
            st.rerun()

def render_chat_interface():
    """Отрисовка интерфейса чата"""
    # Отображение истории сообщений
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Обработка ввода пользователя
    if prompt := st.chat_input("Введите ваше сообщение..."):
        # Добавление сообщения пользователя в историю
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Получение ответа от агента
        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                response = st.session_state.agent.say(prompt)
                st.markdown(response)
        
        # Добавление ответа ассистента в историю
        st.session_state.messages.append({"role": "assistant", "content": response})

def render_auth_interface(auth_manager):
    """Отрисовка интерфейса аутентификации"""
    st.set_page_config(page_title="Авторизация", page_icon="🔐")
    
    st.title("🔐 Авторизация")
    
    # Информация о тестовом пользователе
    with st.expander("Тестовые данные для входа"):
        st.info("""
        **Логин:** demo  
        **Пароль:** 123456
        
        Или зарегистрируйте нового пользователя.
        """)
    
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Логин")
            password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Войти")
            
            if submit:
                if auth_manager.login_user(username, password):
                    st.success("Успешный вход!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Неверный логин или пароль")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Новый логин", placeholder="Введите логин")
            new_password = st.text_input("Новый пароль", type="password", placeholder="Не менее 6 символов")
            confirm_password = st.text_input("Подтвердите пароль", type="password")
            submit_register = st.form_submit_button("Зарегистрироваться")
            
            if submit_register:
                result = auth_manager.register_user(new_username, new_password, confirm_password)
                if result == "success":
                    st.success("Пользователь создан! Теперь вы можете войти.")
                else:
                    st.error(result)