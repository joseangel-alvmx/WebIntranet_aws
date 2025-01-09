const followers = document.getElementById("followers");
async function getfollowers(profileId) {
  const url = "https://www.facebook.com/Alvamex/followers" + profileId + "/?__a=1";
  const response = await fetch(url);
  const data = await response.json();

  return data.graphql.user.edge_followed_by.count;
}

async function setFollowers(profileId) {
  followers.textContent = await getfollowers(profileId);
}

setInterval(() => setFollowers("shariquepathan"), 1000);

//data.graphql.user.profile_pic_url_hd