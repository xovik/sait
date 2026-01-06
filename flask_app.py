from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Настройка API ключа Gemini
API_KEY = "AIzaSyDRwUz5d6mcdUPht7UHCgP7LMJ0mfoOouM"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# Правила сайта для контекста
SITE_RULES = """
Правила Telegram-чата By Step:

1. Уважительное общение - запрещено неадекватное поведение, оскорбление родных, оскорбления, унижения, дискриминация наказание - мут
2. Засорение чата - запрещен спам, флуд, лесенка, капс (>10 слов), флуд смайлами/эмодзи (>10 подряд) наказание - мут
3. Язык общения - основной русский, другие языки в разумных пределах наказание - мут
4. Провокация администрации - запрещено неадекватное общение с администратором наказание - мут
5. Попрошайничество - запрещены просьбы денег, аккаунтов, подписок, донатов наказание - варн/мут
6. Конфликты и провокации - запрещено намеренное разжигание споров наказание -мут
7. Личная информация - запрещено распространять реальные данные без согласия наказание - бан
8. Обход наказания - запрещены любые попытки обойти наказание наказание - бан
9. Выдача себя за других - запрещено воровать аватарки, ники наказание при отказе сменить - бан
10. Выдача себя за By Step - строго запрещено наказание -бан
11. Нарушение правил Telegram - запрещены действия, нарушающие правила Telegram наказание - бан
12. Нарушение законодательства - запрещено обсуждение незаконной деятельности наказание бан
13. Несанкционированная реклама - запрещена любая реклама без разрешения наказание бан на месяц
14. Нарушения Supercell - запрещены продажа, покупка, обмен аккаунтов наказание - бан
15. NSFW контент - запрещены материалы для взрослых наказание - бан
16. Мошенничество - запрещены скам, фишинг, выманивание наказание - бан

Система наказаний:
- Варн - предупреждение, три варна = бан на 1 месяц
- Мут - временный запрет на отправку сообщений
- Бан - полная блокировка доступа к чату
Если вы хотите обжаловать наказание, то напишите админу в тг -@holadnoo
администрация в праве выдавать наказания по своему усмотрению, правила не распростроняются на админов
"""

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Правила Telegram-чата By Step</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Montserrat:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #7B2CBF;
            --primary-light: #9D4EDD;
            --primary-dark: #5A189A;
            --primary-transparent: rgba(123, 44, 191, 0.1);
            --secondary: #FF9E00;
            --secondary-light: #FFB347;
            --dark: #1A1A2E;
            --darker: #0D0D1A;
            --light: #F8F9FA;
            --lighter: #FFFFFF;
            --card-bg: #FFFFFF;
            --danger: #E63946;
            --warning: #F77F00;
            --success: #2A9D8F;
            --info: #3A86FF;
            --text-muted: #4A4E69;
            --text-soft: #6C757D;
            --bg-gradient: linear-gradient(135deg, var(--primary), var(--primary-light));
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --border-radius: 10px;
            --border-radius-lg: 16px;
            --transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            --scroll-percentage: 0%;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--light);
            color: var(--dark);
            line-height: 1.7;
            padding-bottom: 40px;
            font-size: 15px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        header {
            background: var(--bg-gradient);
            color: white;
            padding: 30px 0 35px;
            text-align: center;
            margin-bottom: -20px;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
            border-bottom: 4px solid var(--secondary);
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--primary-light));
            opacity: 0.8;
        }

        .logo {
            font-family: 'Montserrat', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        .logo-icon {
            color: var(--secondary-light);
            font-size: 2rem;
            filter: drop-shadow(0 3px 3px rgba(0, 0, 0, 0.3));
            transform: rotate(-10deg);
        }

        h1 {
            font-size: 1.8rem;
            margin-bottom: 12px;
            font-weight: 700;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .subtitle {
            font-size: 1.1rem;
            opacity: 0.95;
            max-width: 750px;
            margin: 0 auto;
            font-weight: 400;
            line-height: 1.6;
        }

        .version-badge {
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 0.85rem;
            margin-top: 15px;
            display: inline-block;
            font-weight: 700;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
            transition: var(--transition);
        }

        .main-card {
            background: var(--card-bg);
            border-radius: var(--border-radius-lg);
            padding: 30px;
            box-shadow: var(--shadow-lg);
            margin-bottom: 30px;
            border: 1px solid rgba(123, 44, 191, 0.15);
            position: relative;
            z-index: 1;
            overflow: hidden;
        }

        .warning-banner {
            background: linear-gradient(135deg, var(--danger), #ff6b6b);
            color: white;
            padding: 15px 20px;
            border-radius: var(--border-radius);
            margin-bottom: 25px;
            text-align: center;
            font-size: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(229, 57, 53, 0.4);
            border-left: 5px solid white;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }

        .quick-nav {
            display: flex;
            gap: 12px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .nav-btn {
            background: rgba(123, 44, 191, 0.1);
            color: var(--primary);
            padding: 10px 20px;
            border-radius: 30px;
            font-weight: 700;
            text-decoration: none;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(123, 44, 191, 0.2);
            transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }

        .nav-btn:hover {
            background: rgba(123, 44, 191, 0.2);
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(123, 44, 191, 0.25);
        }

        h2 {
            color: var(--primary);
            margin: 30px 0 20px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(123, 44, 191, 0.1);
            font-weight: 800;
            font-family: 'Montserrat', sans-serif;
            position: relative;
        }

        h2::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 3px;
        }

        h2 i {
            font-size: 1.3rem;
            color: var(--secondary);
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .section-description {
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 20px;
            line-height: 1.7;
        }

        .rules-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
        }

        .rule-container {
            position: relative;
        }

        .duration-hint {
            display: none;
            position: absolute;
            top: -8px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--primary);
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.65rem;
            font-weight: 700;
            text-align: center;
            z-index: 2;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.15);
            font-family: 'Montserrat', sans-serif;
            white-space: nowrap;
            transition: var(--transition);
            animation: fadeIn 0.2s ease-out;
            text-transform: none;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateX(-50%) translateY(5px); }
            to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }

        .rule-container.active .duration-hint {
            display: block;
        }

        .rule-container.active .duration-hint::before {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 50%;
            transform: translateX(-50%);
            width: 6px;
            height: 6px;
            background: var(--primary);
            clip-path: polygon(0 0, 100% 0, 50% 100%);
        }

        .rule-card {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            padding: 20px;
            box-shadow: var(--shadow-md);
            border-left: 4px solid var(--primary);
            transition: var(--transition);
            border: 1px solid rgba(123, 44, 191, 0.1);
            position: relative;
            cursor: pointer;
        }

        .rule-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
        }

        .rule-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
        }

        .rule-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }

        .rule-number {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 0.95rem;
            font-weight: 800;
            flex-shrink: 0;
            font-family: 'Montserrat', sans-serif;
            box-shadow: 0 3px 8px rgba(123, 44, 191, 0.4);
        }

        .rule-title {
            font-weight: 800;
            font-size: 1.1rem;
            color: var(--dark);
            letter-spacing: -0.3px;
        }

        .rule-content {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 12px;
            line-height: 1.7;
        }

        .rule-content strong {
            color: var(--dark);
            font-weight: 600;
        }

        .punishments {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 15px;
        }

        .punishment {
            display: inline-flex;
            align-items: center;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 800;
            gap: 5px;
            transition: var(--transition);
        }

        .punishment:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        .mute, .warn {
            background-color: rgba(247, 127, 0, 0.1);
            color: var(--warning);
            border: 1px solid rgba(247, 127, 0, 0.3);
        }

        .ban {
            background-color: rgba(230, 57, 70, 0.1);
            color: var(--danger);
            border: 1px solid rgba(230, 57, 70, 0.3);
        }

        .permanent-ban {
            position: relative;
            padding-right: 25px;
        }

        .permanent-ban::after {
            content: '∞';
            position: absolute;
            top: -5px;
            right: -5px;
            background: var(--danger);
            color: white;
            font-size: 0.7rem;
            font-weight: 900;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .definitions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }

        .definition-card {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            padding: 20px;
            box-shadow: var(--shadow-md);
            border-top: 4px solid var(--primary);
            transition: var(--transition);
            border: 1px solid rgba(123, 44, 191, 0.1);
        }

        .definition-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
        }

        .definition-title {
            color: var(--primary);
            font-weight: 800;
            margin-bottom: 10px;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .definition-title i {
            font-size: 1rem;
            color: var(--secondary);
        }

        .definition-content {
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.7;
        }

        .note-card {
            background: var(--card-bg);
            border-left: 4px solid;
            padding: 20px;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            margin-top: 25px;
            font-size: 0.95rem;
            display: flex;
            gap: 15px;
            color: var(--text-muted);
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(123, 44, 191, 0.1);
            transition: var(--transition);
        }

        .note-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }

        .admin-note {
            border-left-color: var(--primary);
            background: linear-gradient(to right, rgba(123, 44, 191, 0.03), rgba(123, 44, 191, 0.01));
        }

        .appeal-process {
            border-left-color: var(--success);
            background: linear-gradient(to right, rgba(42, 157, 143, 0.05), rgba(42, 157, 143, 0.01));
        }

        .contact-mods {
            border-left-color: var(--info);
            background: linear-gradient(to right, rgba(58, 134, 255, 0.05), rgba(58, 134, 255, 0.01));
        }

        .note-card i {
            font-size: 1.2rem;
            margin-top: 3px;
            flex-shrink: 0;
        }

        .admin-note i {
            color: var(--primary);
        }

        .appeal-process i {
            color: var(--success);
        }

        .contact-mods i {
            color: var(--info);
        }

        .note-content strong {
            display: block;
            margin-bottom: 8px;
            font-size: 1rem;
            color: var(--dark);
            font-weight: 700;
        }

        .highlight-box {
            background: linear-gradient(to right, rgba(255, 158, 0, 0.05), rgba(255, 158, 0, 0.01));
            border-left: 4px solid var(--secondary);
            padding: 18px;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            margin: 20px 0;
            font-size: 1rem;
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
        }

        .highlight-box:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }

        .highlight-box strong {
            display: block;
            margin-bottom: 8px;
            color: var(--dark);
            font-weight: 700;
        }

        footer {
            text-align: center;
            padding: 25px 0;
            color: var(--text-soft);
            font-size: 0.85rem;
            margin-top: 40px;
            position: relative;
        }

        footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(123, 44, 191, 0.4), transparent);
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
        }

        .footer-link {
            color: var(--primary);
            text-decoration: none;
            font-weight: 700;
            font-size: 0.85rem;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 6px;
            position: relative;
        }

        .footer-link::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--primary-light);
            transition: var(--transition);
        }

        .footer-link:hover {
            color: var(--primary-light);
            transform: translateY(-2px);
        }

        .footer-link:hover::after {
            width: 100%;
        }
        .rule-content a {
            color: var(--primary);
            font-weight: 600;
            text-decoration: none;
            border-bottom: 1px dashed var(--primary);
            transition: var(--transition);
        }

        .rule-content a:hover {
            color: var(--primary-dark);
            border-bottom-color: var(--primary-dark);
        }

        /* Модальное окно */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .modal {
            background: var(--card-bg);
            border-radius: var(--border-radius-lg);
            width: 90%;
            max-width: 600px;
            padding: 30px;
            box-shadow: var(--shadow-xl);
            position: relative;
            transform: translateY(20px);
            transition: all 0.3s ease;
        }

        .modal-overlay.active .modal {
            transform: translateY(0);
        }

        .modal-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--text-muted);
            cursor: pointer;
            transition: var(--transition);
        }

        .modal-close:hover {
            color: var(--primary);
            transform: rotate(90deg);
        }

        .modal-title {
            color: var(--primary);
            font-size: 1.5rem;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .modal-links {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }

        .modal-link {
            display: flex;
            align-items: center;
            padding: 15px;
            background: rgba(123, 44, 191, 0.05);
            border-radius: var(--border-radius);
            text-decoration: none;
            color: var(--dark);
            transition: var(--transition);
            border: 1px solid rgba(123, 44, 191, 0.1);
        }

        .modal-link:hover {
            background: rgba(123, 44, 191, 0.1);
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .modal-link-icon {
            width: 40px;
            height: 40px;
            background: var(--primary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: white;
            font-size: 1.2rem;
            flex-shrink: 0;
        }

        .modal-link-content {
            flex: 1;
        }

        .modal-link-title {
            font-weight: 700;
            margin-bottom: 5px;
            color: var(--primary);
        }

        .modal-link-url {
            font-size: 0.85rem;
            color: var(--text-muted);
            word-break: break-all;
            display: none; /* Скрываем URL в контактах */
        }

        /* Кнопка "Наверх" */
        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--primary);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: var(--shadow-lg);
            z-index: 99;
            opacity: 0;
            visibility: hidden;
            transition: var(--transition);
        }

        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }

        .back-to-top::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 2px solid transparent;
            border-top-color: var(--secondary);
            border-right-color: var(--secondary);
            background: conic-gradient(var(--secondary) var(--scroll-percentage), transparent var(--scroll-percentage) 100%);
            animation: none;
        }

        .back-to-top i {
            font-size: 1.2rem;
            position: relative;
            z-index: 1;
        }

        /* Анимации */
        .floating {
            animation: floating 3s ease-in-out infinite;
        }

        @keyframes floating {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
            100% { transform: translateY(0px); }
        }

        /* Стили для AI помощника */
        .ai-assistant {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
        }

        .ai-toggle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--bg-gradient);
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: var(--shadow-xl);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition);
            position: relative;
        }

        .ai-toggle:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 25px rgba(123, 44, 191, 0.4);
        }

        .ai-toggle::after {
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            border-radius: 50%;
            border: 2px solid var(--secondary);
            animation: pulse 2s infinite;
        }

        .ai-chat-container {
            position: absolute;
            bottom: 70px;
            right: 0;
            width: 400px;
            height: 600px;
            background: var(--card-bg);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-xl);
            border: 1px solid rgba(123, 44, 191, 0.15);
            display: none;
            flex-direction: column;
            overflow: hidden;
        }

        .ai-chat-container.active {
            display: flex;
        }

        .ai-chat-header {
            background: var(--bg-gradient);
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .ai-chat-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.1rem;
        }

        .ai-chat-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            transition: var(--transition);
        }

        .ai-chat-close:hover {
            transform: scale(1.1);
        }

        .ai-chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .ai-message {
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.4;
            font-size: 0.9rem;
        }

        .ai-message.user {
            align-self: flex-end;
            background: var(--primary);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .ai-message.bot {
            align-self: flex-start;
            background: var(--light);
            color: var(--dark);
            border: 1px solid rgba(123, 44, 191, 0.1);
            border-bottom-left-radius: 5px;
        }

        .ai-chat-input-container {
            padding: 15px;
            border-top: 1px solid rgba(123, 44, 191, 0.1);
            background: var(--lighter);
        }

        .ai-chat-input-wrapper {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .ai-chat-input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid rgba(123, 44, 191, 0.2);
            border-radius: 25px;
            outline: none;
            font-size: 0.9rem;
            transition: var(--transition);
        }

        .ai-chat-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(123, 44, 191, 0.1);
        }

        .ai-send-button {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--primary);
            border: none;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition);
        }

        .ai-send-button:hover {
            background: var(--primary-dark);
            transform: scale(1.05);
        }

        .ai-send-button:disabled {
            background: var(--text-soft);
            cursor: not-allowed;
            transform: none;
        }

        .ai-typing {
            display: none;
            align-items: center;
            gap: 5px;
            padding: 10px 15px;
            color: var(--text-soft);
            font-size: 0.8rem;
        }

        .ai-typing.active {
            display: flex;
        }

        .typing-dots {
            display: flex;
            gap: 3px;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--primary);
            animation: typing 1.4s infinite ease-in-out;
        }

        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }

        /* Адаптивность */
        @media (max-width: 768px) {
            .container {
                padding: 0 15px;
            }

            header {
                padding: 25px 0 30px;
            }

            .logo {
                font-size: 1.8rem;
            }

            h1 {
                font-size: 1.5rem;
            }

            .subtitle {
                font-size: 1rem;
            }

            .main-card {
                padding: 20px;
            }

            .rules-grid, .definitions-grid {
                grid-template-columns: 1fr;
            }

            .quick-nav {
                gap: 8px;
            }

            .nav-btn {
                padding: 8px 15px;
                font-size: 0.9rem;
            }

            h2 {
                font-size: 1.3rem;
            }

            .duration-hint {
                font-size: 0.6rem;
                padding: 2px 8px;
            }

            .modal {
                width: 95%;
                padding: 20px;
            }

            .modal-links {
                gap: 10px;
            }

            .modal-link {
                padding: 12px;
            }

            .modal-link-icon {
                width: 35px;
                height: 35px;
                font-size: 1rem;
                margin-right: 12px;
            }

            .back-to-top {
                width: 40px;
                height: 40px;
                bottom: 20px;
                right: 20px;
            }

            .ai-chat-container {
                width: 350px;
                height: 500px;
            }

            .ai-assistant {
                bottom: 20px;
                right: 20px;
            }
        }

        @media (max-width: 480px) {
            .ai-chat-container {
                width: 300px;
                height: 450px;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo floating">
                <i class="fab fa-telegram logo-icon"></i>
                By Step
            </div>
            <h1>Правила Telegram-чата</h1>
            <div class="subtitle">Создаём комфортное и безопасное пространство для всех участников. Соблюдайте правила, чтобы избежать наказаний!</div>
        </div>
    </header>

    <div class="container">
        <div class="main-card">
            <div class="warning-banner">
                <i class="fas fa-exclamation-triangle"></i>
                <div>НЕЗНАНИЕ ПРАВИЛ НЕ ОСВОБОЖДАЕТ ОТ ОТВЕТСТВЕННОСТИ. ВНИМАТЕЛЬНО ОЗНАКОМЬТЕСЬ!</div>
            </div>

            <div class="quick-nav">
                <a href="#communication" class="nav-btn">
                    <i class="fas fa-comments"></i> Общение
                </a>
                <a href="#safety" class="nav-btn">
                    <i class="fas fa-shield-alt"></i> Безопасность
                </a>
                <a href="#content" class="nav-btn">
                    <i class="fas fa-photo-video"></i> Контент
                </a>
                <a href="#definitions" class="nav-btn">
                    <i class="fas fa-book"></i> Термины
                </a>
                <a href="#appeal" class="nav-btn">
                    <i class="fas fa-gavel"></i> Апелляции
                </a>
            </div>

            <section id="communication">
                <h2><i class="fas fa-comments"></i> Правила общения</h2>
                <div class="section-description">
                    Основные нормы поведения в чате, которые помогают поддерживать дружелюбную атмосферу и комфортное общение для всех участников.
                </div>

                <div class="rules-grid">
                    <!-- Правило 1 -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность зависит от тяжести</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">1</div>
                                <div class="rule-title">Уважительное общение</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> неадекватное поведение, оскорбление родных, оскорбления, унижения, дискриминация по любым признакам (раса, национальность, гендер, религия, возраст и др.).
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                                <span class="punishment warn"><i class="fas fa-exclamation-circle"></i> Варн</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 2 -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность зависит от колличества</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">2</div>
                                <div class="rule-title">Засорение чата</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> спам, флуд, лесенка, капс (>10 слов), флуд смайлами/эмодзи (>10 подряд), спам командами бота, спам реакциями(>10).
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 3 -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность зависит от колличества</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">3</div>
                                <div class="rule-title">Язык общения</div>
                            </div>
                            <div class="rule-content">
                                <strong>Основной язык:</strong> русский. Другие языки — в разумных пределах, если не мешают общению. Запрещено злоупотребление иностранными языками для затруднения понимания или обхода цензуры. Транслит(eto tak) — только при технических проблемах.
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 4 -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность на усмотрение админа</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">4</div>
                                <div class="rule-title">Провокация администрации</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> неадекватное общение с администратором, провокационные действия, попытки вывести модератора из себя, игнорирование замечаний и требований администрации.
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 5: Попрошайничество -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность на усмотрение админа</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">5</div>
                                <div class="rule-title">Попрошайничество</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> просьбы денег, аккаунтов, подписок, донатов и т.д.
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>

                            </div>
                        </div>
                    </div>

                    <!-- Правило 6: Конфликты и провокации -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность на усмотрение админа</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">6</div>
                                <div class="rule-title">Конфликты и провокации</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> намеренное разжигание споров. Провокационные вопросы и оскорбления с целью создать конфликт.
                            </div>
                            <div class="punishments">
                                <span class="punishment warn"><i class="fas fa-exclamation-circle"></i> Варн</span>
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>

                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="safety">
                <h2><i class="fas fa-shield-alt"></i> Безопасность и конфиденциальность</h2>
                <div class="section-description">
                    Правила, направленные на защиту личных данных, предотвращение вредоносных действий и обеспечение безопасности всех участников чата.
                </div>

                <div class="rules-grid">
                    <!-- Правило 7 -->
                    <div class="rule-container">
                        <div class="duration-hint">Наказание и его длительность зависит от слитой информации</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">7</div>
                                <div class="rule-title">Личная информация</div>
                            </div>
                            <div class="rule-content">
                                <strong>Строго запрещено:</strong> распространять реальные имена, адреса, телефоны, email, фотографии, ссылки на соцсети без согласия человека. Также запрещено собирать и хранить такую информацию без согласия.
                            </div>
                            <div class="punishments">
                                <span class="punishment warn"><i class="fas fa-exclamation-circle"></i> Варн</span>
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                                <span class="punishment ban"><i class="fas fa-ban"></i> Бан</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 8 -->
                    <div class="rule-container">
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">8</div>
                                <div class="rule-title">Обход наказания</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> любые попытки обойти наказание (создание новых аккаунтов, пересоздание аккаунта и т.д.).
                            </div>
                            <div class="punishments">
                                <span class="punishment permanent-ban"><i class="fas fa-skull"></i> Бан</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 9 -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность на усмотрение админа</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">9</div>
                                <div class="rule-title">Выдача себя за других</div>
                            </div>
                            <div class="rule-content">
                                <strong>Запрещено:</strong> воровать аватарки, ники или выдавать себя за другого человека.
                            </div>
                            <div class="punishments">
                                <span class="punishment warn"><i class="fas fa-exclamation-circle"></i> Варн</span>
                                <span class="punishment ban"><i class="fas fa-ban"></i> Бан при отказе сменить</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 10 -->
                    <div class="rule-container">
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">10</div>
                                <div class="rule-title">Выдача себя за By Step</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> выдавать себя за бай степа, связанных личностей или администрацию.
                            </div>
                            <div class="punishments">
                                <span class="punishment permanent-ban"><i class="fas fa-skull"></i> Бан</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 11: Нарушение правил Telegram -->
                    <div class="rule-container">
                        <div class="duration-hint">Длительность зависит от тяжести</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">11</div>
                                <div class="rule-title">Нарушение правил Telegram</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> любые действия, нарушающие <a href="https://telegram.org/tos" target="_blank">правила использования Telegram</a>.
                            </div>
                            <div class="punishments">
                                <span class="punishment ban"><i class="fas fa-ban"></i> Бан</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 12: Нарушение законодательства -->
                    <div class="rule-container">

                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">12</div>
                                <div class="rule-title">Нарушение законодательства</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> обсуждение или пропаганда незаконной деятельности, распространение запрещённых материалов, призывы к насилию, экстремизму и другим действиям, нарушающим законы вашей страны.
                            </div>
                            <div class="punishments">
                                <span class="punishment permanent-ban"><i class="fas fa-skull"></i> Бан</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="content">
                <h2><i class="fas fa-photo-video"></i> Запрещённый контент</h2>
                <div class="section-description">
                    Типы материалов и тем, которые не допускаются к публикации в чате.
                </div>

                <div class="rules-grid">
                    <!-- Правило 13 -->
                    <div class="rule-container">

                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">13</div>
                                <div class="rule-title">Несанкционированная реклама</div>
                            </div>
                            <div class="rule-content">
                                <strong>Запрещено:</strong> любая реклама, реф-ссылки, спам-рассылки, добавление в другие чаты\каналы.
                            </div>
                            <div class="punishments">
                                <span class="punishment ban"><i class="fas fa-ban"></i> Бан месяц</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 14 -->
                    <div class="rule-container">
                        <div class="duration-hint">Наказание и его длительность зависит от тяжести</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">14</div>
                                <div class="rule-title">Нарушения Supercell</div>
                            </div>
                            <div class="rule-content">
                               <strong>Что запрещено:</strong> продажа, покупка, обмен или буст аккаунтов, а также любые другие действия, нарушающие <a href="https://supercell.com/en/terms-of-service/ru/" target="_blank" rel="noopener noreferrer">правила Supercell</a>.
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                                <span class="punishment ban"><i class="fas fa-ban"></i> Бан</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 15 -->
                    <div class="rule-container">
                        <div class="duration-hint">Наказание и его длительность зависит от типа контента</div>
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">15</div>
                                <div class="rule-title"><a href="https://ru.wikipedia.org/wiki/NSFW" target="_blank" rel="noopener noreferrer">NSFW контент</a></div>
                            </div>
                            <div class="rule-content">
                                <strong>Запрещено:</strong> материалы для взрослых, шокирующий, непристойный или запрещенный контент, откровенные изображения/тексты, любые материалы сексуального характера.
                            </div>
                            <div class="punishments">
                                <span class="punishment mute"><i class="fas fa-comment-slash"></i> Мут</span>
                                <span class="punishment ban"><i class="fas fa-ban"></i> Бан</span>
                            </div>
                        </div>
                    </div>

                    <!-- Правило 16 -->
                    <div class="rule-container">
                        <div class="rule-card">
                            <div class="rule-header">
                                <div class="rule-number">16</div>
                                <div class="rule-title">Мошенничество</div>
                            </div>
                            <div class="rule-content">
                                <strong>Что запрещено:</strong> скам, фишинг, выманивание денег/аккаунтов/данных, обман, распространение скам сервисов, вирусов, фишинговых ссылок.
                            </div>
                            <div class="punishments">
                                <span class="punishment permanent-ban"><i class="fas fa-skull"></i> Бан</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="definitions">
                <h2><i class="fas fa-book"></i> Термины и наказания</h2>
                <div class="section-description">
                    Определения и пояснения к системе наказаний в чате.
                </div>

                <div class="definitions-grid">
                    <div class="definition-card">
                        <div class="definition-title"><i class="fas fa-exclamation-triangle"></i> Варн</div>
                        <div class="definition-content">
                            <strong>Предупреждение</strong> за нарушение правил. Три варна = бан на 1 месяц.
                        </div>
                    </div>

                    <div class="definition-card">
                        <div class="definition-title"><i class="fas fa-comment-slash"></i> Мут</div>
                        <div class="definition-content">
                            <strong>Временный запрет</strong> на отправку сообщений. Длительность определяет администратор в зависимости от тяжести нарушения.
                        </div>
                    </div>

                    <div class="definition-card">
                        <div class="definition-title"><i class="fas fa-ban"></i> Бан</div>
                        <div class="definition-content">
                            <strong>Полная блокировка</strong> доступа к чату. Может быть временным или постоянным. Время бана зависит от тяжести нарушения и истории нарушений.
                        </div>
                    </div>
                </div>

                <div class="note-card admin-note">
                    <i class="fas fa-info-circle"></i>
                    <div class="note-content">
                        <strong>Примечание администрации:</strong>
                        Наказания могут меняться в зависимости от контекста, истории нарушений и других факторов. Администрация оставляет за собой право выносить наказания по своему усмотрению. Правила не распространяются на администрацию.
                    </div>
                </div>

                <div id="appeal" class="note-card appeal-process">
                    <i class="fas fa-gavel"></i>
                    <div class="note-content">
                        <strong>Процесс апелляции:</strong>
                        Если вы считаете, что были наказаны несправедливо, вы можете подать апелляцию через ЛС администратора. Укажите: тип наказания, дату, причины несогласия и доказательства. Спам, угрозы, грубость в апелляции приведёт к её отклонению.
                    </div>
                </div>
            </section>
        </div>

        <footer>
            <div class="footer-links">
                <a href="https://t.me/by_step_channel" class="footer-link" target="_blank">
                    <i class="fab fa-telegram"></i> Telegram канал
                </a>

                <a href="#" class="footer-link" id="contact-link">
                    <i class="fas fa-envelope"></i> Контакты
                </a>
            </div>
        </footer>
    </div>

    <!-- AI Помощник -->
    <div class="ai-assistant">
        <button class="ai-toggle" id="ai-toggle">
            <i class="fas fa-robot"></i>
        </button>
        <div class="ai-chat-container" id="ai-chat">
            <div class="ai-chat-header">
                <div class="ai-chat-title">
                    <i class="fas fa-robot"></i>
                    Хомячело
                </div>
                <button class="ai-chat-close" id="ai-close">
                    <i class="fas fa-arrow-left"></i>
                </button>
            </div>
            <div class="ai-chat-messages" id="ai-messages">
                <div class="ai-message bot">
                    Привет! Я Хомячело - AI помощник по правилам чата By Step. Спроси меня о правилах, наказаниях или других вопросах, связанных с чатом!
                </div>
            </div>
            <div class="ai-typing" id="ai-typing">
                <span>Хомячело печатает</span>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
            <div class="ai-chat-input-container">
                <div class="ai-chat-input-wrapper">
                    <input type="text" class="ai-chat-input" id="ai-input" placeholder="Спросите что-нибудь о правилах...">
                    <button class="ai-send-button" id="ai-send">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Кнопка "Наверх" -->
    <div class="back-to-top" id="back-to-top">
        <i class="fas fa-arrow-up"></i>
    </div>

    <!-- Модальное окно контактов -->
    <div class="modal-overlay" id="contact-modal">
        <div class="modal">
            <button class="modal-close" id="modal-close">&times;</button>
            <h2 class="modal-title">
                <i class="fas fa-link"></i> Соц-сети бай степа
            </h2>
            <div class="modal-links">
                <a href="https://t.me/ByStepLive" class="modal-link" target="_blank">
                    <div class="modal-link-icon">
                        <i class="fab fa-telegram"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">Telegram канал</div>
                        <div class="modal-link-url">https://t.me/ByStepLive</div>
                    </div>
                </a>
                <a href="https://t.me/ByStepChatik" class="modal-link" target="_blank">
                    <div class="modal-link-icon" style="background-color: #4CAF50;">
                        <i class="fas fa-comments"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">Основной чат</div>
                        <div class="modal-link-url">https://t.me/ByStepChatik</div>
                    </div>
                </a>
                <a href="https://t.me/bystepfilmcrew" class="modal-link" target="_blank">
                    <div class="modal-link-icon" style="background-color: #FF5722;">
                        <i class="fas fa-film"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">Чат съёмок</div>
                        <div class="modal-link-url">https://t.me/bystepfilmcrew</div>
                    </div>
                </a>
                <a href="https://www.tiktok.com/@_by_step_?_t=8rV6u8AH1zm&_r=1" class="modal-link" target="_blank">
                    <div class="modal-link-icon" style="background-color: #000000;">
                        <i class="fab fa-tiktok"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">TikTok</div>
                        <div class="modal-link-url">https://www.tiktok.com/@_by_step_</div>
                    </div>
                </a>
                <a href="https://www.youtube.com/@bystepYT" class="modal-link" target="_blank">
                    <div class="modal-link-icon" style="background-color: #FF0000;">
                        <i class="fab fa-youtube"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">YouTube</div>
                        <div class="modal-link-url">https://www.youtube.com/@bystepYT</div>
                    </div>
                </a>
                <a href="https://vk.com/1orlov1s" class="modal-link" target="_blank">
                    <div class="modal-link-icon" style="background-color: #0077FF;">
                        <i class="fab fa-vk"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">ВКонтакте</div>
                        <div class="modal-link-url">https://vk.com/1orlov1s</div>
                    </div>
                </a>
                <a href="https://t.me/limoncik83" class="modal-link" target="_blank">
                    <div class="modal-link-icon" style="background-color: #FFC107;">
                        <i class="fas fa-handshake"></i>
                    </div>
                    <div class="modal-link-content">
                        <div class="modal-link-title">Сотрудничество</div>
                        <div class="modal-link-url">https://t.me/limoncik83</div>
                    </div>
                </a>
            </div>
        </div>
    </div>

    <script>
        // Обработчик для карточек с подсказкой о длительности
        document.querySelectorAll('.rule-card').forEach(card => {
            card.addEventListener('click', function(e) {
                e.stopPropagation();
                const container = this.closest('.rule-container');

                // Проверяем, есть ли в этом правиле перманентный бан
                const hasPermanentBan = container.querySelector('.permanent-ban');

                // Если нет перманентного бана, показываем подсказку
                if (!hasPermanentBan) {
                    // Закрываем все другие открытые карточки
                    document.querySelectorAll('.rule-container.active').forEach(otherContainer => {
                        if (otherContainer !== container) {
                            otherContainer.classList.remove('active');
                        }
                    });

                    // Переключаем текущую карточку
                    container.classList.toggle('active');

                    // Прокручиваем к карточке, если подсказка не помещается
                    if (container.classList.contains('active')) {
                        const hint = container.querySelector('.duration-hint');
                        if (hint) {
                            const hintRect = hint.getBoundingClientRect();
                            if (hintRect.top < 0) {
                                container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                            }
                        }
                    }
                }
            });
        });

        // Закрываем подсказки при клике вне карточек
        document.addEventListener('click', function() {
            document.querySelectorAll('.rule-container.active').forEach(container => {
                container.classList.remove('active');
            });
        });

        // Обработчики для модального окна контактов
        const contactLink = document.getElementById('contact-link');
        const contactModal = document.getElementById('contact-modal');
        const modalClose = document.getElementById('modal-close');

        contactLink.addEventListener('click', function(e) {
            e.preventDefault();
            contactModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        modalClose.addEventListener('click', function() {
            contactModal.classList.remove('active');
            document.body.style.overflow = '';
        });

        contactModal.addEventListener('click', function(e) {
            if (e.target === contactModal) {
                contactModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Закрытие по ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && contactModal.classList.contains('active')) {
                contactModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Кнопка "Наверх" с анимацией прогресса
        const backToTopButton = document.getElementById('back-to-top');

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }

            // Обновляем анимацию круга
            const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPosition = window.pageYOffset;
            const scrollPercentage = (scrollPosition / scrollHeight) * 100;
            document.documentElement.style.setProperty('--scroll-percentage', scrollPercentage + '%');
        });

        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Показать длительность наказания при нажатии на бан
        document.querySelectorAll('.punishment.ban:not(.permanent-ban)').forEach(punishment => {
            punishment.addEventListener('click', function(e) {
                e.stopPropagation();
                const duration = this.textContent.match(/\d+/)[0];
                alert(`Наказание по этому правилу: бан на ${duration} дней`);
            });
        });

        // AI Помощник
        const aiToggle = document.getElementById('ai-toggle');
        const aiChat = document.getElementById('ai-chat');
        const aiClose = document.getElementById('ai-close');
        const aiMessages = document.getElementById('ai-messages');
        const aiInput = document.getElementById('ai-input');
        const aiSend = document.getElementById('ai-send');
        const aiTyping = document.getElementById('ai-typing');

        aiToggle.addEventListener('click', function() {
            aiChat.classList.toggle('active');
        });

        aiClose.addEventListener('click', function() {
            aiChat.classList.remove('active');
        });

        function addMessage(text, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `ai-message ${isUser ? 'user' : 'bot'}`;
            messageDiv.textContent = text;
            aiMessages.appendChild(messageDiv);
            aiMessages.scrollTop = aiMessages.scrollHeight;
        }

        function showTyping() {
            aiTyping.classList.add('active');
            aiMessages.scrollTop = aiMessages.scrollHeight;
        }

        function hideTyping() {
            aiTyping.classList.remove('active');
        }

        async function sendMessage() {
            const question = aiInput.value.trim();
            if (!question) return;

            // Добавляем сообщение пользователя
            addMessage(question, true);
            aiInput.value = '';
            aiSend.disabled = true;

            // Показываем индикатор набора
            showTyping();

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });

                const data = await response.json();

                hideTyping();

                if (data.success) {
                    addMessage(data.answer);
                } else {
                    addMessage('Извините, произошла ошибка. Попробуйте позже.');
                }
            } catch (error) {
                hideTyping();
                addMessage('Ошибка соединения. Проверьте интернет и попробуйте снова.');
            }

            aiSend.disabled = false;
        }

        aiSend.addEventListener('click', sendMessage);

        aiInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Открываем чат при первом посещении через 3 секунды
        setTimeout(() => {
            if (!localStorage.getItem('aiChatOpened')) {
                aiChat.classList.add('active');
                localStorage.setItem('aiChatOpened', 'true');
            }
        }, 3000);
    </script>
</body>
</html>
    '''

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        user_question = request.json.get('question', '')

        # Создаем промпт с правилами
        prompt = f"""
        Ты - помощник AI в Telegram-чате By Step. Твоё имя Хомячело. Отвечай ТОЛЬКО на вопросы о правилах чата.

        Правила чата:
        {SITE_RULES}

        Вопрос пользователя: {user_question}

        Ответь кратко и информативно, основываясь строго на правилах сайта.
        Если вопрос не касается правил, вежливо сообщи, что можешь помочь только с вопросами о правилах чата.
        Отвечай на русском языке. Будь дружелюбным и полезным.
        """

        # Отправляем запрос к Gemini API
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = requests.post(GEMINI_URL, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200:
            answer = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({
                'success': True,
                'answer': answer
            })
        else:
            return jsonify({
                'success': False,
                'answer': 'Извините, не удалось получить ответ от AI. Попробуйте позже.'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'answer': f'Извините, произошла ошибка: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)