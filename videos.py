import sys
import re
import urllib.request
import os

from pytube import YouTube

#A function that returns the html text of the playlist link provided through command line
def get_html(playlist_link):
	text = urllib.request.urlopen(playlist_link).read()
	return str(text)

#A function that extracts and returns the playlist id from the playlist link
def get_playlist_id(playlist_link):
	if "list=" in playlist_link:
		start_index = playlist_link.index('=') + 1
		if '&' in playlist_link:
			end_index = playlist_link.index('&')
			playlist_id = playlist_link[start_index:end_index]
		else:
			playlist_id = playlist_link[start_index:]
		return playlist_id

	else:
		print("First argument is not a playlist")
		exit(1)

#A function that converts the string supplied as argument to youtube links of the videos in the playlist
def get_all_links(video_link_matches):
	all_video_links = []
	for video_link_match in video_link_matches:
		if '&' in video_link_match:
			terminate_index = video_link_match.index('&')
		else:
			terminate_index = len(video_link_match)

		all_video_links.append('http://www.youtube.com/' + video_link_match[:terminate_index])

	return all_video_links

#A function that downloads the videos individually
def download_video(num, video_link, directory):
	yt = YouTube(video_link)
	try:
		video = yt.get('mp4', '720p')
	except Exception:
		video = yt.filter('mp4')[-1]
	print(str(num) + ". Downloading: " + yt.filename + "....")
	video.download(path = directory, force_overwrite=True)
	print(yt.filename + " downloaded.\n")



if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Enter playlist link and then path to download directory after python file name")
		exit(1)

	else:
		num = 1
		playlist_link = sys.argv[1]								#A variable that store the link of the playlist
		directory = sys.argv[2]									#A variable that stores the path of the doenload directory
		all_video_links = []
		playlist_id = get_playlist_id(playlist_link)
		html_text = get_html(playlist_link)
		video_link_pattern = re.compile(r'watch\?v=\S+?list=' + playlist_id)		#A variable that stores the suffix pattern of the link of the videos in the playlist
		video_link_matches = list(re.findall(video_link_pattern, html_text))		#A list that stores all the strings that matches above pattern

		if video_link_matches:
			all_video_links = get_all_links(video_link_matches)
		
		final_video_list = []					#A list that will finally have all the video links of the playlist without repetation in the list
		for link in all_video_links:
			flag = 0
			for l in final_video_list:
				if link == l:
					flag = 1
			if flag == 0:
				final_video_list.append(link)

		f = open(os.path.join(directory,"video_links.txt"), "w")		#A file named video_links.txt is created which stores the links of the videos in the playlist
		f.write("These are the links in the playlist you provided:\n\n")
		for video_link in final_video_list:
			f.write(str(num) + ". " + str(video_link) + "\n")
			num = num + 1
		f.close()
		print("There are " + str(len(final_video_list)) + " videos in the playlist.")
		num = 0
		for video_link in final_video_list:
			num = num + 1
			download_video(num, video_link, directory)

		exit(0)			
#program ends
		
