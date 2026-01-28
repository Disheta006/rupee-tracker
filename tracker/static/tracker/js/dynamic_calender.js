function calenderApp() {
    return {
        month: new Date().getMonth(),
        year: new Date().getFullYear(),
        daysOfWeek: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
        monthNames: ['January','February','March','April','May','June','July','August','September','October','November','December'],
        daysWithExpenses: [],
        no_of_days: [],
        blankdays: [],
        totalSpent: window.INITIAL_CALENDER_DATA?.total_spent || 0,
        transactions: window.INITIAL_CALENDER_DATA?.transactions || 0,
        init() {
            this.getNoOfDays();
            this.fetchCalenderDate();
        },

        async fetchCalenderDate() {
            this.daysWithExpenses = [];
            this.totalSpent = 0;
            this.transactions = 0;
            const response = await fetch(
                `/calender/data/?month=${this.month + 1}&year=${this.year}`
            );
            const data = await response.json();
            this.daysWithExpenses = data.expense_days;
            this.totalSpent = data.total_spent;
            this.transactions = data.transactions;
        },

        getNoOfDays() {
            let daysInMonth = new Date(this.year,this.month + 1,0).getDate();
            let dayOfWeek = new Date(this.year,this.month).getDay();
            this.blankdays = Array.from({length:dayOfWeek});
            this.no_of_days = Array.from({length:daysInMonth},(_,i)=>i+1);
        },

        handleDateClick(date) {
            if (!this.hasExpense(date)) return;
            console.log(`clicked $(date)-$(this.month+1)-${this.year}`);
        },
        hasExpense(date) {
            return this.daysWithExpenses.includes(date);
        },
        isToday(date) {
            const today = new Date();
            return today.getDate() === date && today.getMonth() === this.month && today.getFullYear() === this.year;
        },
        previousMonth() {
            if (this.month == 0) {
                this.month = 11;
                this.year--;
            }
            else {
                this.month--;
            }
            this.getNoOfDays();
            this.fetchCalenderDate();
        },
        nextMonth() {
            if (this.month == 11) {
                this.month = 0;
                this.year++;
            }
            else {
                this.month++;
            }
            this.getNoOfDays();
            this.fetchCalenderDate();
        }
    }
}