# Coman & Bassom 2016 — Asymptotic Limits and Wrinkling Patterns in a Pressurised Shallow Spherical Cap

**Источник:** `2_Coman_2016-1.pdf`

## 1. Что именно важно для проекта
- Полезен для понимания **asymptotic structure** неосесимметрической потери устойчивости и особенно **локализации мод near rim**.
- Даёт современную интерпретацию связи между externally / internally pressurised shallow caps и тем, как меняются critical mode number и critical load.
- Для твоего проекта это хороший источник не столько для вывода базовых уравнений, сколько для:
  - проверки ожидаемого поведения `n_cr`;
  - понимания edge-localization;
  - sanity-check asymptotic trends.

## 2. Какие обозначения используются
- Используются собственные безразмерные параметры shallow-cap asymptotics (`μ`, `λ`, `m`, background fields, wrinkling amplitudes и т.п.).
- Номер волны обычно обозначается `m`.
- Формулы записаны в терминах classical shallow-shell asymptotics, а не mixed-weak resultants.

## 3. Какие уравнения / страницы критичны
- **С. 8–10 (Secs. 1–2)** — постановка, геометрия, basic state.
- **После Eq. (2.5)** — важное замечание, что для внешнего и внутреннего давления differential equations почти одинаковы и меняется в основном знак / BC.
- **Sec. 4** — numerical investigation of lowest critical wrinkling pressure.
- **Sec. 5** — asymptotic structure for externally pressurised cap.
- **Формулы типа (5.20)** и соответствующие таблицы/графики — критичны для scaling laws.
- **Sec. 6 / Eq. (6.14)** — параллельный анализ внутреннего давления.

## 4. Где возможны расхождения с твоей моделью
- Это shallow spherical cap asymptotics, а не общая непологая mixed-weak shell-theory.
- В статье нет твоего explicit boundary matrix `B_mix`.
- Использовать как прямой шаблон solver’а нельзя; использовать как ориентир по asymptotic behavior — можно и полезно.

## 5. Можно ли использовать как основной источник
- **Нет, не как основной выводной источник.**
- **Да, как сильный вспомогательный источник по asymptotics и локализации неосесимметрических мод.**
- Статус: **вспомогательный высокого приоритета**.
