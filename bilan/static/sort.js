class SortableTable {
  constructor(tableNode) {
    this.tableNode = tableNode;
    this.columnHeaders = tableNode.querySelectorAll('thead th');
    this.sortColumns = [];

    for (let i = 0; i < this.columnHeaders.length; i++) {
      const ch = this.columnHeaders[i];
      const buttonNode = ch.querySelector('button');
      if (buttonNode) {
        this.sortColumns.push(i);
        ch.setAttribute('aria-sort', 'none');
        buttonNode.setAttribute('data-column-index', i);
        buttonNode.addEventListener('click', this.handleClick.bind(this));
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

window.addEventListener('load', setUpTables);
