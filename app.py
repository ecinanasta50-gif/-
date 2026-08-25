import streamlit as st
import datetime
import json
import random

# Настройка страницы
st.set_page_config(
    page_title="Детективное агентство",
    page_icon="🕵️",
    layout="wide"
)

# Заголовок
st.title("🕵️‍♂️ Детективное агентство «Шерлок»")

# ========== ФУНКЦИЯ ДЛЯ ТАЙМЛАЙНА ==========
def add_timeline_event(case_name, event_type, description):
    """Добавляет событие в таймлайн дела"""
    timeline_key = f"timeline_{case_name}"
    if timeline_key not in st.session_state:
        st.session_state[timeline_key] = []
    
    st.session_state[timeline_key].append({
        "time": datetime.datetime.now().strftime("%H:%M"),
        "date": datetime.datetime.now().strftime("%d.%m.%Y"),
        "type": event_type,
        "description": description
    })

# ========== ФУНКЦИЯ УМНОГО ОТВЕТА ==========
def generate_smart_response(question, suspect_data):
    """
    Генерирует логичный ответ подозреваемого на основе вопроса и его личности
    """
    question_lower = question.lower()
    responses = []
    
    # Базовые ответы в зависимости от личности
    name = suspect_data.get("name", "Подозреваемый")
    alibi = suspect_data.get("alibi", "Не указано")
    motive = suspect_data.get("motive", "Не указан")
    personality = suspect_data.get("personality", "neutral")
    
    # ===== АЛИБИ =====
    if any(word in question_lower for word in ["где", "был", "находился", "место", "алиби", "были"]):
        responses = [
            f"Я был {alibi}. Это точно!",
            f"Как я уже говорил, я был {alibi}. Спросите у кого угодно!",
            f"{alibi} — вот где я был. Можете проверить!",
            f"Я был {alibi}. И я могу это доказать!",
            f"В это время я находился {alibi}. Больше мне нечего добавить."
        ]
        return random.choice(responses)
    
    # ===== МОТИВ =====
    if any(word in question_lower for word in ["зачем", "почему", "мотив", "причина", "за что", "что вам"]):
        if motive and motive != "Не указан":
            responses = [
                f"У меня не было причин! {motive} — это смешно!",
                f"Вы думаете, я бы стал делать такое из-за {motive}? Нет!",
                f"{motive}? Это не повод для преступления!",
                f"Я не стану отрицать, что {motive}, но это не значит, что я виновен!",
                f"Даже если {motive} — это не доказывает мою вину!"
            ]
        else:
            responses = [
                "У меня нет мотива! Я вообще не заинтересован в этом деле!",
                "Какой у меня может быть мотив? Я даже не знал об этом!",
                "Я ничего не выиграл от этого! Зачем мне это делать?"
            ]
        return random.choice(responses)
    
    # ===== СОБЫТИЯ =====
    if any(word in question_lower for word in ["видел", "слышал", "заметил", "наблюдал", "внимание", "что-то"]):
        responses = [
            "Я ничего не видел! Я был занят своими делами.",
            "Может быть, я что-то и заметил, но не придал этому значения...",
            "Я не хочу вас вводить в заблуждение, но я действительно ничего не видел.",
            "Я слышал какой-то шум, но не обратил внимания.",
            "Теперь, когда вы спросили... Мне кажется, я видел кого-то странного."
        ]
        return random.choice(responses)
    
    # ===== ВИНА =====
    if any(word in question_lower for word in ["виновен", "преступление", "сделал", "совершил", "признайся"]):
        if personality == "nervous":
            responses = [
                "Я... я не знаю! Мне страшно! Я ничего не делал!",
                "Пожалуйста, не давите на меня! Я не виновен!",
                "Хорошо, я признаю... что был на месте преступления, но я не убийца!"
            ]
        elif personality == "aggressive":
            responses = [
                "Как вы смеете меня обвинять?! Я ни в чем не виновен!",
                "Это абсурд! Найдите настоящего преступника!",
                "Я вам всё расскажу своему адвокату!"
            ]
        else:
            responses = [
                "Я не виновен. И это единственное, что я вам скажу.",
                "Докажите мою вину. А пока — я свободен.",
                "Я чист перед законом. Можете проверять сколько угодно."
            ]
        return random.choice(responses)
    
    # ===== ЭМОЦИИ =====
    if any(word in question_lower for word in ["как", "чувствуешь", "эмоции", "волнуешься", "переживаешь"]):
        if personality == "nervous":
            responses = [
                "Конечно, я волнуюсь! Меня подозревают в преступлении!",
                "Я на нервах, неужели это не заметно?",
                "Мне очень страшно! Я ничего плохого не делал!"
            ]
        elif personality == "aggressive":
            responses = [
                "Я зол на эту несправедливость!",
                "Меня тошнит от этих допросов!",
                "Я спокоен, потому что знаю, что невиновен!"
            ]
        else:
            responses = [
                "Я спокоен. У меня нет причин волноваться.",
                "Я отношусь к этому философски. Бывает.",
                "Стараюсь сохранять спокойствие."
            ]
        return random.choice(responses)
    
    # ===== ЛИЧНОСТЬ =====
    if any(word in question_lower for word in ["расскажи", "кто ты", "о себе", "чем занимаешься", "работа"]):
        responses = [
            f"Я {name}. И я не хочу говорить о себе.",
            f"Вы знаете моё имя — {name}. Этого достаточно.",
            f"Я обычный человек. У меня есть своя жизнь и работа.",
            f"{name}. Я не вижу смысла рассказывать о себе."
        ]
        return random.choice(responses)
    
    # ===== ОТНОШЕНИЕ К ЖЕРТВЕ =====
    if any(word in question_lower for word in ["жертва", "пострадавший", "знаешь", "знаком"]):
        responses = [
            "Я слышал о пострадавшем. Но лично не знал.",
            "Мне жаль, что это случилось. Но я здесь ни при чём.",
            "Я видел его несколько раз. Но мы не общались.",
            "Я не имею никакого отношения к пострадавшему."
        ]
        return random.choice(responses)
    
    # ===== ОБЩАЯ ФРАЗА ДЛЯ УКЛОНЕНИЯ =====
    generic_responses = [
        f"Я уже всё сказал. Больше мне нечего добавить.",
        "Вы задаёте слишком много вопросов. Я устал.",
        "Я не помню. Это было давно.",
        "Мне нужно подумать. Дайте мне время.",
        "Я не знаю, что вам ответить.",
        "Вы меня запутали своими вопросами.",
        "Это не имеет отношения к делу.",
        "Я хочу поговорить с адвокатом."
    ]
    return random.choice(generic_responses)

# ========== БОКОВОЕ МЕНЮ ==========
with st.sidebar:
    st.header("📂 Мои дела")
    
    if "cases" not in st.session_state:
        st.session_state.cases = {
            "Дело №1": {"client": "Мария Петрова", "status": "Активно", "created": "25.08.2026"}
        }
    
    selected_case = st.selectbox("Выберите дело:", list(st.session_state.cases.keys()))
    
    new_case_name = st.text_input("Название нового дела:")
    if st.button("➕ Создать дело"):
        if new_case_name and new_case_name not in st.session_state.cases:
            st.session_state.cases[new_case_name] = {
                "client": "Не указан", 
                "status": "Активно",
                "created": datetime.datetime.now().strftime("%d.%m.%Y")
            }
            add_timeline_event(new_case_name, "📂 Создание дела", f"Дело '{new_case_name}' открыто")
            st.rerun()
        elif new_case_name:
            st.warning("Такое дело уже существует!")
    
    st.divider()
    st.caption(f"Активных дел: {sum(1 for c in st.session_state.cases.values() if c['status'] == 'Активно')}")
    
    st.divider()
    if st.button("📥 Экспортировать текущее дело", use_container_width=True):
        export_case(selected_case)

# ========== ФУНКЦИЯ ЭКСПОРТА ==========
def export_case(case_name):
    """Создаёт текстовый файл с полным отчётом по делу"""
    
    case_data = st.session_state.cases.get(case_name, {})
    suspects = st.session_state.get(f"suspects_{case_name}", [])
    victims = st.session_state.get(f"victims_{case_name}", [])
    evidence = st.session_state.get(f"evidence_{case_name}", [])
    timeline = st.session_state.get(f"timeline_{case_name}", [])
    
    report = []
    report.append("=" * 60)
    report.append(f"🕵️‍♂️ ДЕТЕКТИВНЫЙ ОТЧЁТ")
    report.append(f"Дело: {case_name}")
    report.append("=" * 60)
    report.append("")
    
    report.append("📋 ОСНОВНАЯ ИНФОРМАЦИЯ")
    report.append(f"Клиент: {case_data.get('client', 'Не указан')}")
    report.append(f"Статус: {case_data.get('status', 'Не указан')}")
    report.append(f"Дата открытия: {case_data.get('created', 'Не указана')}")
    report.append(f"Дата отчёта: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}")
    report.append("")
    
    report.append("=" * 60)
    report.append(f"👤 ПОДОЗРЕВАЕМЫЕ ({len(suspects)})")
    report.append("=" * 60)
    if suspects:
        for i, suspect in enumerate(suspects, 1):
            report.append(f"{i}. {suspect.get('name', 'Без имени')}")
            report.append(f"   Алиби: {suspect.get('alibi', 'Не указано')}")
            report.append(f"   Мотив: {suspect.get('motive', 'Не указан')}")
            report.append(f"   Характер: {suspect.get('personality', 'Не указан')}")
            report.append("")
    else:
        report.append("Подозреваемые не добавлены")
        report.append("")
    
    report.append("=" * 60)
    report.append(f"👥 ПОСТРАДАВШИЕ ({len(victims)})")
    report.append("=" * 60)
    if victims:
        for i, victim in enumerate(victims, 1):
            report.append(f"{i}. {victim.get('name', 'Без имени')}")
            report.append(f"   Контакт: {victim.get('contact', 'Не указан')}")
            report.append(f"   История: {victim.get('story', 'Не указана')}")
            report.append("")
    else:
        report.append("Пострадавшие не добавлены")
        report.append("")
    
    report.append("=" * 60)
    report.append(f"📜 УЛИКИ И ДОКАЗАТЕЛЬСТВА ({len(evidence)})")
    report.append("=" * 60)
    if evidence:
        for i, ev in enumerate(evidence, 1):
            report.append(f"{i}. {ev.get('item', 'Без названия')}")
            report.append(f"   Место находки: {ev.get('location', 'Не указано')}")
            report.append(f"   Описание: {ev.get('notes', 'Нет описания')}")
            report.append("")
    else:
        report.append("Улики не добавлены")
        report.append("")
    
    report.append("=" * 60)
    report.append(f"⏳ ХРОНОЛОГИЯ СОБЫТИЙ ({len(timeline)})")
    report.append("=" * 60)
    if timeline:
        for event in timeline:
            report.append(f"[{event.get('date', '')} {event.get('time', '')}] {event.get('type', '')} - {event.get('description', '')}")
        report.append("")
    else:
        report.append("Событий пока нет")
        report.append("")
    
    # Чаты
    report.append("=" * 60)
    report.append("💬 ИСТОРИЯ ДОПРОСОВ")
    report.append("=" * 60)
    chat_found = False
    for chat_key, messages in st.session_state.get("chats", {}).items():
        if case_name in chat_key:
            chat_found = True
            contact_name = "Неизвестный"
            if "suspect" in chat_key:
                for suspect in suspects:
                    if suspect.get("name", "").lower() in chat_key.lower():
                        contact_name = suspect.get("name", "Подозреваемый")
                        break
            elif "victim" in chat_key:
                for victim in victims:
                    if victim.get("name", "").lower() in chat_key.lower():
                        contact_name = victim.get("name", "Пострадавший")
                        break
            
            report.append(f"\n--- Допрос: {contact_name} ---")
            for msg in messages:
                sender = "Детектив" if msg.get("sender") == "detective" else contact_name
                report.append(f"[{msg.get('time', '')}] {sender}: {msg.get('text', '')}")
            report.append("")
    
    if not chat_found:
        report.append("Допросов не проводилось")
        report.append("")
    
    # Оценка
    report.append("=" * 60)
    report.append("🔍 ИТОГОВАЯ ОЦЕНКА")
    report.append("=" * 60)
    
    missing_alibi = [s["name"] for s in suspects if s.get("alibi", "") == "Не указано" or not s.get("alibi", "")]
    missing_motive = [s["name"] for s in suspects if s.get("motive", "") == "Не указан" or not s.get("motive", "")]
    issues = len(missing_alibi) + len(missing_motive) + max(0, 3 - len(evidence))
    
    if issues == 0:
        report.append("Статус: ✅ ГОТОВО К РАСКРЫТИЮ")
        report.append("Вероятность раскрытия: 98%")
    elif issues <= 3:
        report.append(f"Статус: 🔍 В РАЗРАБОТКЕ")
        report.append(f"Вероятность раскрытия: {80 - issues * 10}%")
        report.append(f"Необходимо устранить проблем: {issues}")
    else:
        report.append(f"Статус: 🚨 ТРЕБУЕТСЯ ИНФОРМАЦИЯ")
        report.append(f"Вероятность раскрытия: {max(5, 30 - issues * 5)}%")
        report.append(f"Необходимо устранить проблем: {issues}")
    
    report.append("")
    report.append("=" * 60)
    report.append("Конец отчёта")
    report.append("=" * 60)
    
    report_text = "\n".join(report)
    
    st.download_button(
        label="📥 Скачать отчёт",
        data=report_text,
        file_name=f"{case_name}_отчёт_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        key="download_report"
    )

# ========== ОСНОВНАЯ ЧАСТЬ ==========
current_case = st.session_state.cases[selected_case]

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Дело", 
    "👤 Подозреваемые", 
    "👥 Пострадавшие", 
    "📜 Улики", 
    "💬 Умный допрос",
    "⏳ Таймлайн",
    "🔍 Проверка"
])

# ========== ВКЛАДКА 1: ДЕЛО ==========
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Информация о деле")
        client_name = st.text_input("Клиент (заказчик):", value=current_case.get("client", ""))
        if st.button("Обновить клиента"):
            old_client = st.session_state.cases[selected_case].get("client", "Не указан")
            st.session_state.cases[selected_case]["client"] = client_name
            if old_client != client_name:
                add_timeline_event(selected_case, "📝 Обновление дела", f"Клиент изменён: {old_client} → {client_name}")
            st.success("Обновлено!")
    
    with col2:
        st.subheader("Статус")
        status = st.selectbox("Статус дела:", ["Активно", "Приостановлено", "Закрыто"], 
                             index=["Активно", "Приостановлено", "Закрыто"].index(current_case["status"]))
        if st.button("Изменить статус"):
            old_status = st.session_state.cases[selected_case]["status"]
            st.session_state.cases[selected_case]["status"] = status
            if old_status != status:
                add_timeline_event(selected_case, "📊 Изменение статуса", f"Статус изменён: {old_status} → {status}")
            st.success(f"Статус изменен на {status}")
    
    st.divider()
    st.caption(f"Дело создано: {current_case.get('created', 'Неизвестно')}")

# ========== ВКЛАДКА 2: ПОДОЗРЕВАЕМЫЕ ==========
with tab2:
    st.subheader("👤 Список подозреваемых")
    st.info("💡 При создании подозреваемого укажите его ФИО, характер и другие данные. Это повлияет на его ответы на допросе!")
    
    case_key = f"suspects_{selected_case}"
    if case_key not in st.session_state:
        st.session_state[case_key] = [
            {
                "name": "Мистер Мурзик", 
                "alibi": "на крыше", 
                "motive": "Ревность", 
                "personality": "nervous",
                "age": "35",
                "profession": "Безработный"
            },
            {
                "name": "Соседка Зина", 
                "alibi": "дома смотрела сериал", 
                "motive": "Хотела нового кота", 
                "personality": "aggressive",
                "age": "55",
                "profession": "Пенсионерка"
            }
        ]
        for suspect in st.session_state[case_key]:
            add_timeline_event(selected_case, "👤 Добавление подозреваемого", f"Добавлен {suspect['name']}")
    
    for i, suspect in enumerate(st.session_state[case_key]):
        with st.expander(f"🕵️ {suspect['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input(f"ФИО #{i}", value=suspect["name"], key=f"name_{i}_{selected_case}")
                new_alibi = st.text_area(f"Алиби #{i}", value=suspect["alibi"], key=f"alibi_{i}_{selected_case}")
                new_motive = st.text_area(f"Мотив #{i}", value=suspect["motive"], key=f"motive_{i}_{selected_case}")
                
            with col2:
                st.write("**Личные данные:**")
                new_age = st.text_input(f"Возраст #{i}", value=suspect.get("age", ""), key=f"age_{i}_{selected_case}")
                new_profession = st.text_input(f"Профессия #{i}", value=suspect.get("profession", ""), key=f"prof_{i}_{selected_case}")
                
                personality_options = {
                    "neutral": "😐 Нейтральный",
                    "nervous": "😰 Нервный", 
                    "aggressive": "😠 Агрессивный",
                    "calm": "😌 Спокойный",
                    "mysterious": "🤫 Таинственный"
                }
                current_personality = suspect.get("personality", "neutral")
                new_personality = st.selectbox(
                    f"Характер #{i}", 
                    options=list(personality_options.keys()),
                    format_func=lambda x: personality_options[x],
                    index=list(personality_options.keys()).index(current_personality) if current_personality in personality_options else 0,
                    key=f"pers_{i}_{selected_case}"
                )
            
            col3, col4 = st.columns(2)
            with col3:
                if st.button(f"💬 Начать допрос #{i}", key=f"chat_{i}_{selected_case}"):
                    st.session_state[f"chat_open_{selected_case}_{i}"] = True
                    st.rerun()
            with col4:
                if st.button(f"Обновить данные #{i}", key=f"update_{i}_{selected_case}"):
                    old_name = st.session_state[case_key][i]["name"]
                    st.session_state[case_key][i]["name"] = new_name
                    st.session_state[case_key][i]["alibi"] = new_alibi
                    st.session_state[case_key][i]["motive"] = new_motive
                    st.session_state[case_key][i]["age"] = new_age
                    st.session_state[case_key][i]["profession"] = new_profession
                    st.session_state[case_key][i]["personality"] = new_personality
                    if old_name != new_name:
                        add_timeline_event(selected_case, "✏️ Изменение данных", f"Подозреваемый переименован: {old_name} → {new_name}")
                    st.success("Обновлено!")
            
            if st.button(f"❌ Удалить #{i}", key=f"delete_{i}_{selected_case}"):
                deleted_name = st.session_state[case_key][i]["name"]
                st.session_state[case_key].pop(i)
                add_timeline_event(selected_case, "🗑️ Удаление", f"Удалён подозреваемый {deleted_name}")
                st.rerun()
    
    with st.expander("➕ Добавить подозреваемого"):
        st.write("Заполните все данные для создания полноценной личности:")
        new_suspect_name = st.text_input("ФИО подозреваемого:")
        new_suspect_alibi = st.text_area("Алиби:")
        new_suspect_motive = st.text_area("Мотив:")
        new_suspect_age = st.text_input("Возраст:")
        new_suspect_profession = st.text_input("Профессия:")
        new_suspect_personality = st.selectbox(
            "Характер:",
            options=["neutral", "nervous", "aggressive", "calm", "mysterious"],
            format_func=lambda x: {
                "neutral": "😐 Нейтральный",
                "nervous": "😰 Нервный", 
                "aggressive": "😠 Агрессивный",
                "calm": "😌 Спокойный",
                "mysterious": "🤫 Таинственный"
            }[x]
        )
        
        if st.button("➕ Добавить подозреваемого"):
            if new_suspect_name:
                st.session_state[case_key].append({
                    "name": new_suspect_name,
                    "alibi": new_suspect_alibi if new_suspect_alibi else "Не указано",
                    "motive": new_suspect_motive if new_suspect_motive else "Не указан",
                    "age": new_suspect_age if new_suspect_age else "Не указан",
                    "profession": new_suspect_profession if new_suspect_profession else "Не указана",
                    "personality": new_suspect_personality
                })
                add_timeline_event(selected_case, "👤 Добавление подозреваемого", f"Добавлен {new_suspect_name}")
                st.success("Подозреваемый добавлен!")
                st.rerun()
            else:
                st.warning("Введите имя подозреваемого!")

# ========== ВКЛАДКА 3: ПОСТРАДАВШИЕ ==========
with tab3:
    st.subheader("👥 Пострадавшие (заказчики)")
    
    victims_key = f"victims_{selected_case}"
    if victims_key not in st.session_state:
        st.session_state[victims_key] = [
            {"name": "Мария Петрова", "contact": "8-999-123-45-67", "story": "Пропал любимый кот Барсик"},
        ]
        for victim in st.session_state[victims_key]:
            add_timeline_event(selected_case, "👥 Добавление пострадавшего", f"Добавлен {victim['name']}")
    
    for i, victim in enumerate(st.session_state[victims_key]):
        with st.expander(f"👤 {victim['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                v_name = st.text_input(f"Имя пострадавшего #{i}", value=victim["name"], key=f"v_name_{i}_{selected_case}")
                v_contact = st.text_input(f"Контакт #{i}", value=victim["contact"], key=f"v_contact_{i}_{selected_case}")
            with col2:
                v_story = st.text_area(f"История #{i}", value=victim["story"], key=f"v_story_{i}_{selected_case}")
            
            col3, col4 = st.columns(2)
            with col3:
                if st.button(f"💬 Связаться с пострадавшим #{i}", key=f"chat_victim_{i}_{selected_case}"):
                    st.session_state[f"chat_victim_open_{selected_case}_{i}"] = True
                    st.rerun()
            
            if st.button(f"Обновить данные пострадавшего #{i}", key=f"v_update_{i}_{selected_case}"):
                old_name = st.session_state[victims_key][i]["name"]
                st.session_state[victims_key][i] = {"name": v_name, "contact": v_contact, "story": v_story}
                if old_name != v_name:
                    add_timeline_event(selected_case, "✏️ Изменение данных", f"Пострадавший переименован: {old_name} → {v_name}")
                st.success("Обновлено!")
    
    with st.expander("➕ Добавить пострадавшего"):
        v_name = st.text_input("Имя пострадавшего:")
        v_contact = st.text_input("Контакт:")
        v_story = st.text_area("История:")
        if st.button("Добавить пострадавшего"):
            st.session_state[victims_key].append({"name": v_name, "contact": v_contact, "story": v_story})
            add_timeline_event(selected_case, "👥 Добавление пострадавшего", f"Добавлен {v_name}")
            st.success("Добавлен!")
            st.rerun()

# ========== ВКЛАДКА 4: УЛИКИ ==========
with tab4:
    st.subheader("📜 Улики и доказательства")
    
    evidence_key = f"evidence_{selected_case}"
    if evidence_key not in st.session_state:
        st.session_state[evidence_key] = [
            {"item": "Клочок шерсти", "location": "Диван", "notes": "Серого цвета"},
            {"item": "Следы лап", "location": "Кухня", "notes": "В муке"}
        ]
        for ev in st.session_state[evidence_key]:
            add_timeline_event(selected_case, "📜 Добавление улики", f"Добавлена улика: {ev['item']}")
    
    cols = st.columns(3)
    for i, evidence in enumerate(st.session_state[evidence_key]):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"**🔍 {evidence['item']}**")
                st.write(f"📍 {evidence['location']}")
                st.write(f"📝 {evidence['notes']}")
                if st.button(f"❌ Удалить #{i}", key=f"ev_del_{i}_{selected_case}"):
                    deleted_ev = st.session_state[evidence_key][i]["item"]
                    st.session_state[evidence_key].pop(i)
                    add_timeline_event(selected_case, "🗑️ Удаление", f"Удалена улика: {deleted_ev}")
                    st.rerun()
    
    with st.expander("➕ Добавить улику"):
        item = st.text_input("Название улики:")
        location = st.text_input("Место находки:")
        notes = st.text_area("Описание:")
        if st.button("Добавить улику"):
            if item:
                st.session_state[evidence_key].append({"item": item, "location": location, "notes": notes})
                add_timeline_event(selected_case, "📜 Добавление улики", f"Добавлена улика: {item}")
                st.success("Улика добавлена!")
                st.rerun()

# ========== ВКЛАДКА 5: УМНЫЙ ДОПРОС ==========
with tab5:
    st.subheader("💬 Умный допрос")
    st.info("🤖 Подозреваемые отвечают на ваши вопросы логично, исходя из их характера и данных!")
    
    if "chats" not in st.session_state:
        st.session_state.chats = {}
    
    suspects = st.session_state.get(case_key, [])
    victims = st.session_state.get(victims_key, [])
    
    all_contacts = []
    for i, suspect in enumerate(suspects):
        all_contacts.append({
            "id": f"suspect_{i}",
            "name": suspect["name"],
            "type": "Подозреваемый",
            "index": i,
            "is_suspect": True,
            "data": suspect
        })
    
    for i, victim in enumerate(victims):
        all_contacts.append({
            "id": f"victim_{i}",
            "name": victim["name"],
            "type": "Пострадавший",
            "index": i,
            "is_suspect": False,
            "data": victim
        })
    
    if not all_contacts:
        st.info("Добавьте подозреваемых или пострадавших, чтобы начать допрос!")
    else:
        contact_names = [f"{c['type']}: {c['name']}" for c in all_contacts]
        selected_contact_idx = st.selectbox("Выберите собеседника:", range(len(contact_names)), 
                                           format_func=lambda x: contact_names[x])
        selected_contact = all_contacts[selected_contact_idx]
        chat_id = f"chat_{selected_case}_{selected_contact['id']}"
        
        if chat_id not in st.session_state.chats:
            st.session_state.chats[chat_id] = []
            add_timeline_event(selected_case, "💬 Начало допроса", f"Начат допрос: {selected_contact['name']}")
        
        # Показываем профиль допрашиваемого
        with st.expander("📋 Профиль допрашиваемого", expanded=False):
            if selected_contact["is_suspect"]:
                data = selected_contact["data"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ФИО:** {data.get('name', 'Не указано')}")
                    st.write(f"**Возраст:** {data.get('age', 'Не указан')}")
                with col2:
                    st.write(f"**Профессия:** {data.get('profession', 'Не указана')}")
                    st.write(f"**Характер:** {data.get('personality', 'Не указан')}")
                st.write(f"**Алиби:** {data.get('alibi', 'Не указано')}")
                st.write(f"**Мотив:** {data.get('motive', 'Не указан')}")
            else:
                data = selected_contact["data"]
                st.write(f"**ФИО:** {data.get('name', 'Не указано')}")
                st.write(f"**Контакт:** {data.get('contact', 'Не указан')}")
                st.write(f"**История:** {data.get('story', 'Не указана')}")
        
        st.divider()
        chat_container = st.container(height=400)
        
        with chat_container:
            if st.session_state.chats[chat_id]:
                for msg in st.session_state.chats[chat_id]:
                    if msg["sender"] == "detective":
                        st.markdown(f"**🕵️ Вы:** {msg['text']}")
                        st.caption(f"_{msg['time']}_")
                    else:
                        emoji = "👤"
                        if selected_contact["is_suspect"]:
                            personality = selected_contact["data"].get("personality", "neutral")
                            emoji = {
                                "nervous": "😰",
                                "aggressive": "😠",
                                "calm": "😌",
                                "mysterious": "🤫"
                            }.get(personality, "👤")
                        st.markdown(f"**{emoji} {selected_contact['name']}:** {msg['text']}")
                        st.caption(f"_{msg['time']}_")
                    st.write("---")
            else:
                st.info(f"Начните допрос {selected_contact['name']}. Задайте вопрос!")
        
        # Подсказки для вопросов
        with st.expander("💡 Подсказки для допроса", expanded=False):
            st.markdown("""
            **Какие вопросы можно задать:**
            - 🕵️ **Об алиби:** *"Где вы были в момент преступления?"*
            - 🕵️ **О мотиве:** *"Зачем вам это было нужно?"*
            - 🕵️ **О событиях:** *"Вы видели что-то подозрительное?"*
            - 🕵️ **О вине:** *"Вы признаёте свою вину?"*
            - 🕵️ **Об эмоциях:** *"Как вы себя чувствуете?"*
            - 🕵️ **О личности:** *"Расскажите о себе!"*
            - 🕵️ **О жертве:** *"Вы знали пострадавшего?"*
            
            💡 Подозреваемый отвечает логично, исходя из своего характера и данных!
            """)
        
        col1, col2 = st.columns([5, 1])
        with col1:
            new_message = st.text_input("Ваш вопрос:", key=f"msg_input_{chat_id}", 
                                       placeholder="Например: Где вы были вчера вечером?")
        with col2:
            send_button = st.button("📤 Отправить", key=f"send_{chat_id}")
        
        if send_button and new_message:
            # Добавляем вопрос детектива
            st.session_state.chats[chat_id].append({
                "sender": "detective",
                "text": new_message,
                "time": datetime.datetime.now().strftime("%H:%M")
            })
            add_timeline_event(selected_case, "💬 Вопрос на допросе", 
                             f"Вопрос к {selected_contact['name']}: {new_message[:40]}...")
            
            # Генерируем умный ответ
            if selected_contact["is_suspect"]:
                suspect_data = selected_contact["data"]
                response = generate_smart_response(new_message, suspect_data)
            else:
                # Для пострадавших — простые ответы
                victim_responses = [
                    "Я очень переживаю!",
                    "Пожалуйста, найдите виновного!",
                    "Я не знаю, что ещё сказать...",
                    "Это ужасно!",
                    "Я надеюсь на вашу помощь!"
                ]
                response = random.choice(victim_responses)
            
            st.session_state.chats[chat_id].append({
                "sender": "contact",
                "text": response,
                "time": datetime.datetime.now().strftime("%H:%M")
            })
            st.rerun()
        
        # Дополнительные кнопки
        col3, col4, col5 = st.columns(3)
        with col3:
            if st.button("🔄 Сгенерировать ответ заново", key=f"regenerate_{chat_id}"):
                # Берем последний вопрос детектива
                last_msgs = st.session_state.chats[chat_id]
                detective_questions = [m for m in last_msgs if m["sender"] == "detective"]
                if detective_questions:
                    last_question = detective_questions[-1]["text"]
                    # Удаляем последний ответ контакта
                    if last_msgs and last_msgs[-1]["sender"] == "contact":
                        last_msgs.pop()
                    
                    if selected_contact["is_suspect"]:
                        suspect_data = selected_contact["data"]
                        response = generate_smart_response(last_question, suspect_data)
                    else:
                        response = "Я уже всё сказал."
                    
                    st.session_state.chats[chat_id].append({
                        "sender": "contact",
                        "text": response,
                        "time": datetime.datetime.now().strftime("%H:%M")
                    })
                    st.rerun()
        
        with col4:
            if st.button("🗑️ Очистить историю", key=f"clear_{chat_id}"):
                st.session_state.chats[chat_id] = []
                st.rerun()
        
        with col5:
            if st.button("📋 Показать все улики", key=f"show_evidence_{chat_id}"):
                evidence_list = st.session_state.get(evidence_key, [])
                if evidence_list:
                    ev_text = "📜 Улики по делу:\n" + "\n".join([f"- {e['item']} ({e['location']})" for e in evidence_list])
                    st.session_state.chats[chat_id].append({
                        "sender": "detective",
                        "text": ev_text,
                        "time": datetime.datetime.now().strftime("%H:%M")
                    })
                    st.rerun()
                else:
                    st.warning("Улик пока нет!")
        
        st.divider()
        col6, col7 = st.columns(2)
        with col6:
            msg_count = len(st.session_state.chats[chat_id])
            st.metric("💬 Всего сообщений", msg_count)
        with col7:
            detective_msgs = sum(1 for m in st.session_state.chats[chat_id] if m["sender"] == "detective")
            contact_msgs = msg_count - detective_msgs
            st.metric("📊 Соотношение", f"{detective_msgs} : {contact_msgs}")

# ========== ВКЛАДКА 6: ТАЙМЛАЙН ==========
with tab6:
    st.subheader("⏳ Хронология событий по делу")
    
    timeline_key = f"timeline_{selected_case}"
    if timeline_key not in st.session_state:
        st.session_state[timeline_key] = []
    
    timeline = st.session_state[timeline_key]
    
    if not timeline:
        st.info("Пока нет событий. Начните расследование!")
    else:
        dates = {}
        for event in timeline:
            date = event.get("date", "Неизвестно")
            if date not in dates:
                dates[date] = []
            dates[date].append(event)
        
        for date, events in sorted(dates.items(), reverse=True):
            st.markdown(f"### 📅 {date}")
            for event in events:
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.write(f"**{event.get('time', '')}**")
                with col2:
                    st.write(f"{event.get('type', '')} - {event.get('description', '')}")
            st.divider()
        
        st.subheader("📊 Статистика событий")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Всего событий", len(timeline))
        with col2:
            suspect_events = sum(1 for e in timeline if "подозреваем" in e.get("description", "").lower())
            st.metric("По подозреваемым", suspect_events)
        with col3:
            evidence_events = sum(1 for e in timeline if "улик" in e.get("description", "").lower())
            st.metric("По уликам", evidence_events)

# ========== ВКЛАДКА 7: ПРОВЕРКА ТЕОРИЙ ==========
with tab7:
    st.subheader("🔍 Проверка детективных теорий")
    
    suspects = st.session_state.get(case_key, [])
    evidence_list = st.session_state.get(evidence_key, [])
    timeline = st.session_state.get(timeline_key, [])
    
    st.write(f"**Всего подозреваемых:** {len(suspects)}")
    st.write(f"**Всего улик:** {len(evidence_list)}")
    st.write(f"**Событий в таймлайне:** {len(timeline)}")
    
    st.subheader("Автоматический анализ:")
    
    missing_alibi = [s["name"] for s in suspects if s.get("alibi", "") == "Не указано" or not s.get("alibi", "")]
    if missing_alibi:
        st.warning(f"⚠️ У следующих подозреваемых нет алиби: {', '.join(missing_alibi)}")
    else:
        st.success("✅ У всех подозреваемых есть алиби!")
    
    if len(evidence_list) < 3:
        st.warning(f"⚠️ Мало улик! Всего {len(evidence_list)}, нужно хотя бы 3 для полноценного расследования")
    else:
        st.success(f"✅ Улик достаточно: {len(evidence_list)}")
    
    missing_motive = [s["name"] for s in suspects if s.get("motive", "") == "Не указан" or not s.get("motive", "")]
    if missing_motive:
        st.warning(f"⚠️ У следующих подозреваемых нет мотива: {', '.join(missing_motive)}")
    else:
        st.success("✅ У всех подозреваемых есть мотив!")
    
    chat_count = len([c for c in st.session_state.get("chats", {}).keys() if selected_case in c])
    if chat_count > 0:
        st.success(f"✅ Проведено {chat_count} допросов/бесед")
    else:
        st.warning("⚠️ Ещё не было проведено ни одного допроса!")
    
    if len(timeline) > 5:
        st.success(f"✅ Хорошая хронология: {len(timeline)} событий")
    elif len(timeline) > 0:
        st.info(f"ℹ️ В деле {len(timeline)} событий. Добавьте больше активности!")
    else:
        st.warning("⚠️ В деле нет ни одного события!")
    
    st.divider()
    issues = len(missing_alibi) + len(missing_motive) + max(0, 3 - len(evidence_list)) + (1 if chat_count == 0 else 0)
    
    if issues == 0:
        st.balloons()
        st.success("🎉 ДЕЛО ГОТОВО К РАСКРЫТИЮ! Все данные собраны!")
        st.write("**Вероятность раскрытия:** 98%")
    elif issues <= 3:
        st.info(f"🔍 Дело близится к разгадке! Осталось устранить {issues} неточностей")
        st.write(f"**Вероятность раскрытия:** {80 - issues * 10}%")
    else:
        st.error(f"🚨 Требуется больше информации! Найдено {issues} проблем")
        st.write(f"**Вероятность раскрытия:** {max(5, 30 - issues * 5)}%")
    
    if suspects:
        st.subheader("📊 Профили подозреваемых")
        for suspect in suspects:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{suspect['name']}**")
                st.write(f"Алиби: {suspect.get('alibi', 'Не указано')}")
                st.write(f"Мотив: {suspect.get('motive', 'Не указан')}")
                st.write(f"Характер: {suspect.get('personality', 'Не указан')}")
            with col2:
                suspicious_score = 0
                if suspect.get('alibi', '') == "Не указано" or not suspect.get('alibi', ''):
                    suspicious_score += 1
                if suspect.get('motive', '') == "Не указан" or not suspect.get('motive', ''):
                    suspicious_score += 1
                if "не" in suspect.get('alibi', '').lower():
                    suspicious_score += 1
                
                if suspicious_score >= 3:
                    st.error("🔴 Высокая степень подозрения")
                elif suspicious_score >= 1:
                    st.warning("🟡 Требуется дополнительная проверка")
                else:
                    st.success("🟢 Низкая степень подозрения")
