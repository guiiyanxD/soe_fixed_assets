/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { DateField } from "@web/views/fields/date/date_field";

patch(DateField.prototype, {
    setup() {
        this._super(...arguments);
    },

    async onValueUpdate(value) {
        await this._super(value);

        const fieldName = this.props.name;

        if (fieldName === "return_date") {
            const loanDate = this.props.record.data.loan_date;
            const returnDate = value;

            if (loanDate && returnDate && returnDate < loanDate) {
                this.env.services.notification.add("⚠️ La fecha de devolución no puede ser anterior a la fecha de préstamo.", {
                    type: "danger",
                });
            }
        }
    },
});
