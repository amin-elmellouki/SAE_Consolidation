window.addEventListener('load', function () {
    const cells = document.querySelectorAll('td[data-note]');
    
    cells.forEach(cell => {
        const value = parseFloat(cell.getAttribute('data-note'));
        
        if (value >= 15) {
            cell.style.backgroundColor = 'rgba(0, 255, 0, 0.5)';
            cell.style.color = 'black';
        } else if (value >= 10) {
            cell.style.backgroundColor = 'rgba(154, 205, 50, 0.5)';
            cell.style.color = 'black';
        } else if (value >= 5) {
            cell.style.backgroundColor = 'rgba(255, 165, 0, 0.5)';
            cell.style.color = 'black';
        } else {
            cell.style.backgroundColor = 'rgba(255, 0, 0, 0.5)';
            cell.style.color = 'black';
        }
    });
});