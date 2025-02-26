class SortableTable {
  constructor(tableNode) {
    this.tableNode = tableNode;
    this.columnHeaders = tableNode.querySelectorAll('thead th');
    this.sortColumns = [];
    this.filterColumnIndex = null;
    this.filterButton = null;
    this.filterPopup = null;

    for (let i = 0; i < this.columnHeaders.length; i++) {
      const ch = this.columnHeaders[i];
      const buttonNode = ch.querySelector('button');
      if (buttonNode) {
        this.sortColumns.push(i);
        ch.setAttribute('aria-sort', 'none');
        buttonNode.setAttribute('data-column-index', i);
        
        const filterIcon = buttonNode.querySelector('.material-symbols-rounded');
        if (filterIcon && filterIcon.textContent.includes('filter_alt')) {
          console.log("Filter button found:", buttonNode);
          this.filterButton = buttonNode;
          buttonNode.addEventListener('click', this.handleFilterClick.bind(this));
          this.setupFilterPopup(ch, buttonNode, i);
          this.filterColumnIndex = i;
        } else {
          buttonNode.addEventListener('click', this.handleClick.bind(this));
        }
      }
    }

    this.optionCheckbox = document.querySelector(
      'input[type="checkbox"][value="show-unsorted-icon"]'
    );

    if (this.optionCheckbox) {
      this.optionCheckbox.addEventListener(
        'change',
        this.handleOptionChange.bind(this)
      );
      if (this.optionCheckbox.checked) {
        this.tableNode.classList.add('show-unsorted-icon');
      }
    }
  }

  setupFilterPopup(headerCell, filterButton, columnIndex) {
    const filterPopup = document.createElement('div');
    filterPopup.className = 'filter-popup';
    filterPopup.style.display = 'none';
    filterPopup.style.position = 'absolute';
    filterPopup.style.backgroundColor = 'white';
    filterPopup.style.boxShadow = '0px 8px 16px 0px rgba(0,0,0,0.2)';
    filterPopup.style.zIndex = '1000';
    filterPopup.style.borderRadius = '8px';
    filterPopup.style.padding = '10px';
    filterPopup.style.minWidth = '150px';
    filterPopup.style.maxHeight = '300px';
    filterPopup.style.overflowY = 'auto';
    
    const allOption = document.createElement('div');
    allOption.className = 'filter-option';
    allOption.textContent = 'Toutes les matières';
    allOption.style.padding = '8px 12px';
    allOption.style.cursor = 'pointer';
    allOption.style.borderRadius = '4px';
    allOption.addEventListener('mouseover', () => {
      allOption.style.backgroundColor = '#f1f1f1';
    });
    allOption.addEventListener('mouseout', () => {
      allOption.style.backgroundColor = 'transparent';
    });
    allOption.addEventListener('click', () => {
      this.applyFilter('all');
      filterPopup.style.display = 'none';
    });
    filterPopup.appendChild(allOption);
    
    const matieres = new Set();
    const rows = this.tableNode.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
      if (row.cells[columnIndex]) {
        const demandeConso = row.cells[columnIndex].textContent.trim();
        if (demandeConso && demandeConso !== '❌') {
          const matieresText = demandeConso.replace('✅', '').trim();
          if (matieresText) {
            matieresText.split(',').forEach(matiere => {
              matieres.add(matiere.trim());
            });
          }
        }
      }
    });
    
    matieres.forEach(matiere => {
      const option = document.createElement('div');
      option.className = 'filter-option';
      option.textContent = matiere;
      option.style.padding = '8px 12px';
      option.style.cursor = 'pointer';
      option.style.borderRadius = '4px';
      option.addEventListener('mouseover', () => {
        option.style.backgroundColor = '#f1f1f1';
      });
      option.addEventListener('mouseout', () => {
        option.style.backgroundColor = 'transparent';
      });
      option.addEventListener('click', () => {
        this.applyFilter(matiere);
        filterPopup.style.display = 'none';
      });
      filterPopup.appendChild(option);
    });
    
    document.body.appendChild(filterPopup);
    
    this.filterPopup = filterPopup;
    this.filterButton = filterButton;
  }
  
  handleFilterClick(event) {
    event.stopPropagation();
    
    if (!this.filterButton || !this.filterPopup) {
      console.error("Filter button or popup not initialized");
      return;
    }
    
    const buttonRect = this.filterButton.getBoundingClientRect();
    this.filterPopup.style.top = (buttonRect.bottom + window.scrollY) + 'px';
    this.filterPopup.style.left = (buttonRect.left + window.scrollX) + 'px';
    
    if (this.filterPopup.style.display === 'none') {
      this.filterPopup.style.display = 'block';
      
      const closeFilterPopup = (e) => {
        if (!this.filterPopup.contains(e.target) && e.target !== this.filterButton){
          this.filterPopup.style.display = 'none';
          document.removeEventListener('click', closeFilterPopup);
        }
      };
      
      setTimeout(() => {
        document.addEventListener('click', closeFilterPopup);
      }, 0);
    } else {
      this.filterPopup.style.display = 'none';
    }
  }
  
  applyFilter(matiere) {
    if (this.filterColumnIndex === null) {
      console.error("Filter column index not set");
      return;
    }

    const rows = this.tableNode.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
      if (matiere === 'all') {
        row.style.display = '';
      } else {
        const cell = row.cells[this.filterColumnIndex];
        if (cell) {
          const demandeConso = cell.textContent.trim();
          if (demandeConso.includes('✅') && demandeConso.includes(matiere)) {
            row.style.display = '';
          } else {
            row.style.display = 'none';
          }
        }
      }
    });
    
    if (this.filterButton) {
      if (matiere === 'all') {
        this.filterButton.innerHTML = 'Demande conso. <span style="margin-right: 10px; font-size: 1.4em;" class="material-symbols-rounded">filter_alt</span>';
      } else {
        this.filterButton.innerHTML = `Filtre: ${matiere} <span style="margin-right: 10px; font-size: 1.4em;" class="material-symbols-rounded">filter_alt</span>`;
      }
    }
  }

  setColumnHeaderSort(columnIndex) {
    if (typeof columnIndex === 'string') {
      columnIndex = parseInt(columnIndex);
    }

    for (let i = 0; i < this.columnHeaders.length; i++) {
      const ch = this.columnHeaders[i];
      const buttonNode = ch.querySelector('button');
      if (i === columnIndex) {
        const value = ch.getAttribute('aria-sort');
        if (value === 'descending') {
          ch.setAttribute('aria-sort', 'ascending');
          this.sortColumn(
            columnIndex,
            'ascending',
            ch.classList.contains('num')
          );
        } else if (value === 'ascending') {
          ch.setAttribute('aria-sort', 'descending');
          this.sortColumn(
            columnIndex,
            'descending',
            ch.classList.contains('num')
          );
        } else {
          ch.setAttribute('aria-sort', 'ascending');
          this.sortColumn(
            columnIndex,
            'ascending',
            ch.classList.contains('num')
          );
        }
      } else {
        if (ch.hasAttribute('aria-sort') && buttonNode) {
          ch.setAttribute('aria-sort', 'none');
        }
      }
    }
  }

  handleClick(event) {
    const tgt = event.currentTarget;
    this.setColumnHeaderSort(tgt.getAttribute('data-column-index'));
  }

  handleOptionChange(event) {
    const tgt = event.currentTarget;
    if (tgt.checked) {
      this.tableNode.classList.add('show-unsorted-icon');
    } else {
      this.tableNode.classList.remove('show-unsorted-icon');
    }
  }

  sortColumn(columnIndex, direction, isNumeric) {
    const tbody = this.tableNode.querySelector('tbody');
    const rows = Array.from(tbody.rows);

    const parseNumber = (str) => {
      const cleaned = str.replace(/,/g, '').replace(/[^0-9.-]/g, '');
      const num = parseFloat(cleaned);
      return isNaN(num) ? null : num;
    };

    rows.sort((rowA, rowB) => {
      const cellA = rowA.cells[columnIndex].textContent.trim();
      const cellB = rowB.cells[columnIndex].textContent.trim();

      if (isNumeric) {
        const numA = parseNumber(cellA) || 0;
        const numB = parseNumber(cellB) || 0;
        return direction === 'ascending' ? numA - numB : numB - numA;
      } else {
        const numA = parseNumber(cellA);
        const numB = parseNumber(cellB);

        if (numA !== null && numB !== null) {
          return direction === 'ascending' ? numA - numB : numB - numA;
        } else {
          return direction === 'ascending'
            ? cellA.localeCompare(cellB)
            : cellB.localeCompare(cellA);
        }
      }
    });

    while (tbody.firstChild) {
      tbody.removeChild(tbody.firstChild);
    }

    rows.forEach(row => tbody.appendChild(row));
  }
}

function setUpTables() {
  const sortableTables = document.querySelectorAll('table.sortable');
  for (const table of sortableTables) {
    new SortableTable(table);
  }
}

window.addEventListener('DOMContentLoaded', setUpTables);