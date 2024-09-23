document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleSidebarButton = document.getElementById('toggle-sidebar');

    // Mostrar/Ocultar o painel lateral
    toggleSidebarButton.addEventListener('click', function () {
        sidebar.classList.toggle('is-hidden-touch');
    });

    // Função para mostrar/ocultar submenus com animação
    window.toggleMenu = function (menuId) {
        const menu = document.getElementById(menuId);
        if (menu.classList.contains('is-hidden')) {
            menu.classList.remove('is-hidden');
            menu.style.maxHeight = menu.scrollHeight + 'px';
        } else {
            menu.style.maxHeight = 0;
            setTimeout(() => menu.classList.add('is-hidden'), 300);
        }
    };
});
