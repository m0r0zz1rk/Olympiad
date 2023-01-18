<template>
    <slot name="side-chb"></slot>
    <div class="side-panel">
        <label class="side-button-2" for="side-checkbox">+</label>
        <div class="side-title">
            <slot name="sidebox-title"></slot>
        </div>
        <slot name="sidebox-text"></slot>
        <table style="margin: 0 auto; table-layout: fixed; width: 100%;">
           <tbody class="sidebox-table-trs">
                <slot name="main-table-trs"></slot>
           </tbody>
        </table>
        <br>
        <slot name="sidebox-button"></slot>
        <br><br>
        <div class="advanced-sidebox">
            <div class="side-advanced-title">
                <slot name="sidebox-advanced-title"></slot>
            </div>
            <table style="margin: 0 auto; table-layout: fixed; width: 100%;" class="fl-table">
               <tbody class="advanced-table-trs">
                 <slot name="advanced-table-trs"></slot>
               </tbody>
            </table>
            <br>
        <slot name="adv-sidebox-button"></slot>
        </div>
    </div>
</template>

<script>

export default {
        name: 'SideBox',
    }
</script>

<style>
/* Оформление панели */
#side-checkbox {
    display: none;
}
.side-advanced-title {
    color: #00415d;
    text-align: center;
    font-size: 20px;
}
.sidebox-active {
  display: block;
  visibility: visible;
  pointer-events: auto;
}
.sidebox-deactive {
  display: none;
  visibility: collapse;
  pointer-events: none;
}
.side-panel {
    position: fixed;
    z-index: 16;
    top: 0;
    right: -40vw;
    background: #FFF;
    color: #00415d;
    transition: all 0.5s;
    width: 40vw;
    height: 100vh;
    box-shadow: 10px 0 20px rgba(0,0,0,0.4);
    padding: 40px 20px;
}
.side-title {
    color: #00415d;
    text-align: center;
    font-size: 20px;
    padding-bottom: 10px;
    margin-bottom: 20px;
    border-bottom: 2px solid #00415d;
}
/* Оформление кнопки на странице */
.side-button-1-wr {
    text-align: center; /* Контейнер для кнопки, чтобы было удобнее ее разместить */
}
.side-button-1 {
    display: inline-block;
}
.side-button-1 .side-b {
    margin: 5px;
    width: 130px;
    text-decoration: none;
    position: relative;
    font-weight: bold;
    line-height: 20px;
    padding: 6px 15px;
    color: #FFF;
    background: #373c59;
    cursor: pointer;
    border-radius: 15px;
}
.side-button-1 .side-b:hover,
.side-button-1 .side-b:active,
.side-button-1 .side-b:focus {
    color: #FFF;
}
.side-button-1 .side-b:after,
.side-button-1 .side-b:before {
    position: absolute;
    height: 4px;
    left: 50%;
    bottom: -6px;
    content: "";
    transition: all 280ms ease-in-out;
    width: 0;
}
/*.side-button-1 .side-open:after,
.side-button-1 .side-open:before {
    background: green;
}*/
.side-button-1 .side-close:after,
.side-button-1 .side-close:before {
    background: red;
}
.side-button-1 .side-b:before {
    top: -6px;
}
.side-button-1 .side-b:hover:after,
.side-button-1 .side-b:hover:before {
    width: 100%;
    left: 0;
}
/* Переключатели кнопки 1 */
.side-button-1 .side-close {
    display: none;
}
#side-checkbox:checked + .side-panel + .side-button-1-wr .side-button-1 .side-open {
    display: none;
}
#side-checkbox:checked + .side-panel + .side-button-1-wr .side-button-1 .side-close {
    display: block;
}
#side-checkbox:checked + .side-panel {
    right: 0;
}
/* Оформление кнопки на панеле */
.side-button-2 {
    font-size: 30px;
    border-radius: 20px;
    position: absolute;
    z-index: 1;
    top: 8px;
    left: 8px;
    cursor: pointer;
    transform: rotate(45deg);
    color: #000000;
    transition: all 280ms ease-in-out;
}
.side-button-2:hover {
    transform: rotate(45deg) scale(1.1);
    color: #f15c4e;
}
tr.border_bottom td {
  border-bottom: 1px solid #373c59;
}
</style>