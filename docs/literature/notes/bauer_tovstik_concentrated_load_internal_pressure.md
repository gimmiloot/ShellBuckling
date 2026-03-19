# Bauer & Tovstik — Buckling of Spherical Shells under Concentrated Load and Internal Pressure

**Источник:** `BauerTovstik.pdf`

## 1. Что именно важно для проекта
- Полезен как дополнительный источник по схеме:
  - axisymmetric pre-buckling state;
  - adjacent equilibrium problem;
  - mode competition under changing prestress/background.
- Для твоего проекта важен не конкретный load case (concentrated load + internal pressure), а то, как authors separate asymptotic inner deformation zone and unsymmetric mode selection.

## 2. Какие обозначения используются
- В осесимметрической части используются `U`, `V`, `M_1`, `M_2`, `ε_1`, `ε_2`, angle `θ`, small parameter `μ`.
- Для adjacent equilibrium появляется Donnell-type система для `w(ξ)` и `Φ(ξ)` с wave number `m`.
- Это отдельный notation world; прямого совпадения с твоими текущими обозначениями нет.

## 3. Какие уравнения / страницы критичны
- **С. 1–2** — equations of axisymmetric deformation.
- **Формулы (1)–(2)** — starting point for pre-buckling state.
- **С. 4** — Donnell system `(9)–(10)` for adjacent equilibrium and definitions of `k_i`, `t_i`.
- **С. 5** — results table showing change of critical load with internal pressure and mode number.

## 4. Где возможны расхождения с твоей моделью
- Совсем другой loading case и другая asymptotic regime.
- Есть Donnell shallow-shell reduction, а не твой current mixed-weak general shell route.
- Полезно как analogy / reference, но не как template for current solver.

## 5. Можно ли использовать как основной источник
- **Нет.**
- Статус: **вспомогательный низкого приоритета**.
