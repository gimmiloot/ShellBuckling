# Makowski & Stumpf 1989 — Finite Axisymmetric Deformation of Shells of Revolution

**Источник:** `bf00534312.pdf`

## 1. Что именно важно для проекта
- Это один из самых близких к твоей задаче источников по логике **“точный / более общий осесимметрический фон → вариационная постановка → уравнения критического равновесия”**.
- Особенно ценен тем, что авторы явно строят геометрию и работу-conjugate measures для **shells of revolution**, а не только для plate/FvK-модели.
- Для текущего проекта полезен как опора для:
  - корректной геометрии осесимметрического background;
  - аккуратного разделения strain measures и conjugate stress-resultants;
  - вариационного маршрута вместо ad hoc closure.

## 2. Какие обозначения используются
- Используются геометрические переменные для оболочки вращения в цилиндрических координатах: `r(s)`, `z(s)`, stretches `λ_s`, `λ_θ`, curvature-type quantities, rotation angle и associated stress/couple resultants.
- Есть собственная система обозначений для strain energy, work-conjugate measures и incremental constitutive relations.
- Эти обозначения не совпадают с твоими `u_s,u_n,varphi,...`, но хорошо ложатся на текущую идею “corrected geometry + conjugate pairs”.

## 3. Какие уравнения / страницы критичны
- **С. 456–460 (Sect. 2)** — геометрия деформации оболочки вращения, базовые кinematic assumptions и определение deformed triad.
- **Sect. 3** — strain measures и conjugate stress measures.
- **Sect. 4** — variational / critical-equilibrium layer; это важный ориентир для твоего перехода к weak-form.
- **Sect. 5** — constitutive properties, которые авторы сами называют crucial for large-strain boundary value problems.
- **Sect. 6** — application to flexural buckling of circular plates и reduction to nonlinear eigenvalue problem.

## 4. Где возможны расхождения с твоей моделью
- У статьи material model — hyperelastic incompressible shell и большой акцент на finite strain.
- Твоя текущая рабочая модель — другая по физическим предпосылкам и не обязана наследовать весь constitutive block этой статьи.
- Полезно брать **геометрическую и вариационную дисциплину**, но не механически переносить материал-специфические формулы.

## 5. Можно ли использовать как основной источник
- **Да, как основной источник по общей осесимметрической геометрии и variational route.**
- **Осторожно** использовать как прямой источник конкретных constitutive relations.
- Статус: **основной**.
