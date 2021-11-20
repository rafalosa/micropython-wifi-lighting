<html>
<head><title>ESP LED color strip</title>

</head>
<link rel="stylesheet" href='static/website.css'>
<body>
<div class="outer-container">
    <div class="left-sub">
        <form action="" method="post">
            <label class="power-switch">
                <input name="power_switch" onChange="this.form.submit()" type="checkbox" {%if a[1]== True%} checked
                       {%endif%}>
                <span class="power-slider"></span>
            </label></form>
        <form action="" method="post">

            <div class="modes-container">

                <button name="pulse_but" type="submit" class="mode-pulse-button" {%if a[2]== 0 and a[3] !=0 %}
                        style="background-color: #3779ff; color: white;" {% endif %} {%if a[3]== 0%} disabled {%endif%}>
                    PULSE
                </button>
                <button name="trans_but" type="submit" class="mode-transition-button" {%if a[2]== 1 and a[3] !=0 %}
                        style="background-color: #3779ff; color: white;" {% endif %} {%if a[3]== 0%} disabled {%endif%}>
                    COLOR TRANS.
                </button>
                <button name="static_but" type="submit" class="mode-static-button" {%if a[2]== 2 and a[3] !=0 %}
                        style="background-color: #3779ff; color: white;" {% endif %} {%if a[3]== 0%} disabled {%endif%}>
                    STATIC
                </button>

            </div>
        </form>
    </div>
    <form action="" method="post">
        <div class="right-sub">
            <input name="color_picker" type="color" class="color-picker" {%if a[3]== 0%} disabled {%endif%}>
            <button name="reprog_but" type="submit" class="reprogram-button" {%if a[3]== 0%} disabled {%endif%}>{%if a[3] == 2%}CONFIRM{%else%}CHANGE COLORS{%endif%}
            </button>
            <div class="status-container">

                <p class="status">STATUS: {{a[0]}}</p>

            </div>
        </div>
    </form>

</div>
</body>

</html>