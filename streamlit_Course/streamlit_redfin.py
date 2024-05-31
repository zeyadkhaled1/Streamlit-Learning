import streamlit as st
import asyncio
import nest_asyncio
import streamlit_shadcn_ui as ui
import redfin_async_streamlit as redfin

# Set Streamlit configuration
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")
nest_asyncio.apply()
    

@st.cache_data(show_spinner=False)
def scrape_data_sync():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(redfin.main())

def remove_character(df, column_name,characters_to_remove):
    df[column_name] = df[column_name].str.replace(characters_to_remove, '').astype(float)
    return df


    
def update_authenticated_wrapper(credits_correct:bool):
    def update_authenticated():
        if credits_correct:
            st.session_state["authenticated"]=True
    return update_authenticated

def check_authentication():
    if st.session_state.get("authenticated",False):
        return True
    user_name = st.text_input("Your email")
    password = st.text_input("Enter Your Password", type="password")
    credits_correct=True if user_name=="Sean Nearing" and password=="Sean123" else False
    submit=st.button(label="Submit", on_click=update_authenticated_wrapper(credits_correct))
    if submit:
        if credits_correct:
            st.session_state["authenticated"]=True
            return True
        else:
            st.error("Invalid Credentials")
            return False
        
# Main function to control the scraping process and display the dashboard
async def main():
    # Button to initiate scraping
    sign_in_allowed=check_authentication()
    if not sign_in_allowed:
        return
    ui_button=ui.button(text="Scrape Data", key="trigger_btn")
    if ui_button:
        scrape_data_sync.clear()
    with st.spinner('Scraping data... This will take up to 3 minutes.'):
        # Scrape data
        data = scrape_data_sync()
        st.success('Data scraping complete!')

        # Display the rest of the dashboard
        show_dashboard(data)


# Function to display the dashboard
def show_dashboard(df):
    # Title of the dashboard
    st.title("Real Estate Market Dashboard")

       # Calculate useful statistics
    st.subheader("Statistics")
    df = remove_character(df, "Solds Homes (30 Days)",",")
    df = remove_character(df, "Listed Homes (All)",",")
    df=remove_character(df,"Ratio Homes","%")
    total_sold_30_days = df['Solds Homes (30 Days)'].sum()
    total_listed_all = df['Listed Homes (All)'].sum()
    average_sold_30_days = df['Solds Homes (30 Days)'].mean()
    average_listed_all = df['Listed Homes (All)'].mean()
    average_ratio_homes = df['Ratio Homes'].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        ui.metric_card(title="Total Sold Homes (30 Days)", content=str(total_sold_30_days))
        ui.metric_card(title="Total Listed Homes (All)", content=str(total_listed_all))

    with col2:
        ui.metric_card(title="Average Sold Homes (30 Days)", content=f"{average_sold_30_days:.2f}")
        ui.metric_card(title="Average Listed Homes (All)", content=f"{average_listed_all:.2f}")

    with col3:
        ui.metric_card(title="Average Ratio of Homes Sold (30 Days)", content=f"{average_ratio_homes:.2f}%")


    # Dataframe search functionality
    st.subheader("Search in Data") 
    search_term = st.text_input("Enter County Name or Part of it:")
    filtered_df = df[df['County'].str.contains(search_term, case=False, na=False)]
    st.dataframe(filtered_df,use_container_width=True)

    
    # Footer
    st.markdown("""
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: #f1f1f1;
                text-align: center;
                padding: 10px;
                font-size: 12px;
            }
        </style>
        <div class="footer">
            <p>Real Estate Market Dashboard - Data as of 2024-05-30</p>
        </div>
        """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    asyncio.run(main())
