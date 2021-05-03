<html>
<head><title>ESP LED color strip</title>
    <style>
      :root {
        --left-width: 190px;
        --outer-width: 400px;
        --outer-height: 400px;
        --universal-margin_hor: 15px;
        --universal-margin_ver: 30px;
        --button-width: 130px;
        --button-height: 75px;
        --mode-button-padding: 0px;
        --power-rep-button-padding: 25px;
        --button-font-size: 20px;
        --color-picker-height: 50px;
        --color-picker-width: 50px;
      }

      div[class*="container"] {
        border: 2px solid;
        border-radius: 10px;
        border-color: #c9c9c9;
        margin: var(--universal-margin_hor);
      }

      .modes-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
      }

      div[class*="sub"] {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
      }

      html {
        font-family: Helvetica;
        display: inline-block;
        margin: 0 auto;
      }

      .outer-container {
        height: var(--outer-height);
        width: var(--outer-width);
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
      }

      .left-sub {
        float: left;
        width: var(--left-width);
      }

      .right-sub {
        float: left;
        width: calc(var(--outer-width) - var(--left-width) - 2*var(--universal-margin_hor));
          margin-top: 50px;
      }

      button{
        width: var(--button-width);
        height: var(--button-height);
        margin: var(--universal-margin_hor);
        font-size: var(--button-font-size);
        transition-duration: 0.1s;
        border: none;
        text-decoration: none;
        border-radius: 5px;
      }

      button[class*="mode"]:disabled + .reprogram-button:disabled{

          background-color: #c9c9c9;
          color: #e3e3e3;

      }

      button[class*="mode"]:enabled{
        background-color: #dedede;
        color: black;
      }

      button[class*="mode"]:hover:enabled{
        background-color: #3779ff;
        color: white;
      }

       button:active:enabled{
         transform: translateY(2px);
      }

      .reprogram-button:enabled {
        background-color: #d97676;
        color: white;

      }
      .reprogram-button{
          width: 100px;
          height: 100px;
      }

      .reprogram-button:hover:enabled {
        background-color: #df5555;
        color: white;
      }

      .color-picker{
        width: var(--color-picker-width);
        height: var(--color-picker-height);
        margin: var(--universal-margin_ver) 15px ;
      }

      .power-switch {
        position: relative;
        top: 20px;
        display: inline-block;
        width: 60px;
        height: 34px;
      }

.power-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.power-slider {

  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #d97676;
  -webkit-transition: .4s;
  transition: .8s;
  border-radius: 34px;
}

.power-slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;

  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 34px;
}

input:checked + .power-slider {
  background-color: #76d987;
}

input:focus + .power-slider {
}

input:checked + .power-slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
  border-radius: 50%;
}
      .status{
        font-size:16px;
      }

      .status-container{

        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        height: 70px;
          width: 170px;

      }
        .status-container{

            background-color: #c1ffcc;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            text-align: center;

        }

    </style>
</head>
<body>
<div class="outer-container">
<div class="left-sub">
  <form action="" method="post">
<label class="power-switch">
  <input name="power_switch" onChange="this.form.submit()" type="checkbox" {%if a[1] == True%} checked {%endif%}>
  <span class="power-slider"></span>
</label></form>
    <form action="" method="post">

  <div class="modes-container">

    <button name="pulse_but" type="submit" class="mode-pulse-button" {%if a[2] == 0 and a[3] !=0 %} style="background-color: #3779ff; color: white;"{% endif %} {%if a[3] == 0%} disabled {%endif%}>PULSE</button>
    <button name="trans_but" type="submit" class="mode-transition-button" {%if a[2] == 1 and a[3] !=0 %} style="background-color: #3779ff; color: white;"{% endif %} {%if a[3] == 0%} disabled {%endif%}>COLOR TRANS.</button>
    <button name="static_but" type="submit" class="mode-static-button" {%if a[2] == 2 and a[3] !=0 %} style="background-color: #3779ff; color: white;"{% endif %} {%if a[3] == 0%} disabled {%endif%}>STATIC</button>

  </div></form></div>
    <form action="" method="post">
        <div class="right-sub">
<input name="color_picker" type="color" class="color-picker"  {%if a[3] == 0%} disabled {%endif%}>
<button name="reprog_but" type="submit" class="reprogram-button"  {%if a[3] == 0%} disabled {%endif%}>{%if a[3] == 2%}CONFIRM{%else%}CHANGE COLORS{%endif%}</button>
      <div class="status-container">

    <p class="status">STATUS: {{a[0]}}</p>

    </div></div></form>

</div>
</body>
</html>