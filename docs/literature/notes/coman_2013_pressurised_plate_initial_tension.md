# Coman 2013 — Asymmetric Bifurcations in a Pressurised Circular Thin Plate under Initial Tension

**Источник:** `3_Coman 2013 - Asymmetric bifurcations in a pressurised.pdf`

## 1. Что именно важно для проекта
- Полезен как компактный пример того, как строится задача **adjacent equilibrium** для circular plate на фоне уже напряжённого осесимметрического состояния.
- Особенно важен как современный короткий шаблон:
  - постановка background state;
  - гармоническая ansatz для asymmetric perturbations;
  - boundary-layer / edge-localisation interpretation.
- Для проекта это удобный reference, когда нужно быстро вспомнить структуру plate bifurcation problem без длинной книги.

## 2. Какие обозначения используются
- Фон описывается через in-plane displacement и transverse displacement; perturbations обозначаются через functions `U`, `V`, `W` или аналогичные радиальные амплитуды.
- Номер волны идёт как `m`.
- Используется language of initial tension / pre-stress, что полезно для сопоставления с твоим prestress-block, хотя не совпадает с твоей mixed-weak нотацией.

## 3. Какие уравнения / страницы критичны
- **С. 11–12** — постановка и смысл bifurcation from pressurised state.
- **С. 13** — derivation of the adjacent-equilibrium problem.
- **Формулы (17a)–(17b)** — boundary conditions.
- **Формулы около (18)** — regularity / center conditions.
- **Заключение** — qualitative dependence of critical load and wrinkle number on background tension and localization.

## 4. Где возможны расхождения с твоей моделью
- Это thin plate with initial tension, не общая shell of revolution.
- Нет твоих moment/shear resultants и boundary matrix language.
- Источник хорошо работает как conceptual cross-check, но не как буквальная база для текущего mixed-weak solver’а.

## 5. Можно ли использовать как основной источник
- **Нет, как основной — нет.**
- **Да, как компактный вспомогательный источник по adjacent-equilibrium logic и edge localisation.**
- Статус: **вспомогательный**.
