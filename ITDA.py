import streamlit as st
from streamlit_gsheets import GSheetsConnection
from functions import *

def main():
    conn = st.connection("gsheets", type=GSheetsConnection)

    data1 = conn.read(worksheet="Sheet1", ttl=30)
    data2 = conn.read(worksheet="Sheet2", ttl=30)
    
    st.subheader("MUJ Members Sheet")
    with st.spinner("Loading Data"):
        st.dataframe(data1)

    query1 = '''
    SELECT "Name","Reg No.","Email ID"
    FROM Sheet1
    WHERE "PAYMENT(FINANCE)" is NOT NULL
    AND "PORTAL(ITDA)" is NULL;
    '''

    with st.expander("View New Members"):
        with st.spinner():
            new_members = conn.query(query1)
            st.write(new_members)

    if st.button("Update Database"):
        with st.spinner("Updating..."):
            updated_members1 = data1.copy()
            updated_members1.loc[(updated_members1["PORTAL(ITDA)"].isnull()) & (~updated_members1["PAYMENT(FINANCE)"].isnull()), "PORTAL(ITDA)"] = "DONE (CORRECTED)"

            for _, row in new_members.iterrows():
                name = row["Name"]
                email = row["Email ID"]
                add_to_firebase(email, name)

            conn.update(worksheet="Test", data=updated_members1)
            st.success("Database Updated Successfully")
    
    st.subheader("Outstations Members Sheet")
    with st.spinner():
        st.dataframe(data2)

    query2 = '''
    SELECT "Name", "Email", "Contact"
    FROM "Sheet2"
    WHERE "PAYMENT(FINANCE)" is NOT NULL
    AND "PORTAL(ITDA)" is NULL;
    '''

    with st.expander("View New Members"):
        with st.spinner():
            non_muj_new_members = conn.query(query2)
            st.table(non_muj_new_members)

    if st.button("Update NON MUJ Database"):
        with st.spinner("Updating..."):
            updated_members2 = data2.copy()
            updated_members2.loc[(updated_members2["PORTAL(ITDA)"].isnull()) & (~updated_members2["PAYMENT(FINANCE)"].isnull()), "PORTAL(ITDA)"] = "DONE (CORRECTED)"

            try:
                for _, row in non_muj_new_members.iterrows():
                    name = row["Name"]
                    email = row["Email"]
                    add_to_firebase(email, name)
            except Exception as e:
                st.error(e)

            st.success("Database Updated Successfully")

if __name__ == "__main__":
    main()