# Bauer–Semenov–Voronkova–Dorofeev — Asymmetric Buckling of Circular and Annular Plates under Normal Pressure

**Источник:** `holm3.pdf` (глава 2 в сборнике)

## 1. Что именно важно для проекта
- Это очень полезный проектный источник, потому что он связывает:
  - analytical shallow-shell/plate model,
  - FEM/ANSYS comparisons,
  - поведение **annular / hinged** cases,
  - qualitative shift of modes and edge behavior.
- Главный practically important message для твоего проекта: при росте нагрузки расхождение между FEM и shallow-shell equations растёт, а для **hinged support** нужен переход к **general theory of shells**.
- Это почти прямое литературное подкрепление твоей рабочей стратегии: сначала стабилизировать физически корректный background, а не считать найденный shallow-like срыв окончательным `q_cr`.

## 2. Какие обозначения используются
- Глава работает в plate/shallow-shell notation через transverse displacement `w`, stress function `F`, mode number `n`, bending stiffness `D(r)` и т.п.
- Есть и homogeneous, и radially inhomogeneous plate cases, а также annular plate.
- Прямого соответствия твоим mixed-weak полям нет.

## 3. Какие уравнения / страницы критичны
- **Chapter pages 19–20** — introduction and problem formulation.
- **Eq. (2.1)–(2.5)** — базовая shallow-shell/plate постановка.
- **Chapter pages 23–27** — numerical results, FEM comparison, annular plates.
- **Chapter page 28 / Conclusion** — самый важный для проекта вывод:
  shallow-shell equations increasingly misrepresent subcritical state at higher loads; for plates with hinged support at the outer edge one should use the **general theory of shells**.

## 4. Где возможны расхождения с твоей моделью
- Глава не выводит твою mixed-weak постановку и не даёт `B_mix`.
- Это всё ещё shallow-shell / plate-level source.
- Но как раз поэтому она ценна: она объясняет, **почему** shallow-level подход может перестать быть достаточным именно там, где у тебя сейчас начинается проблема.

## 5. Можно ли использовать как основной источник
- **Да, как основной источник по физической интерпретации ошибки shallow-background при hinged support.**
- **Нет, как основной источник для вывода окончательных mixed-weak equations.**
- Статус: **основной ориентир по simple-support / FEM / интерпретации**.
